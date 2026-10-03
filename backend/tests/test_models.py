import pytest
from sqlalchemy import create_engine, event, inspect, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.db.base import Base
from app.models import (
    Album, ArtistProfile, AuditLog, BlogCategory, BlogPost, BlogTag, Comment,
    CommentStatus, ContactMessage, ContentStatus, DownloadEvent, GalleryItem,
    MediaFile, MediaKind, PlayEvent, SiteSetting, Song, SocialLink, User, UserRole,
    Video, VideoViewEvent,
)

EXPECTED_TABLES = {
    "users", "artist_profiles", "albums", "songs", "videos", "blog_posts",
    "blog_categories", "blog_tags", "post_tags", "comments", "gallery_items",
    "contact_messages", "social_links", "media_files", "site_settings",
    "play_events", "download_events", "video_view_events", "audit_logs",
}


@pytest.fixture()
def engine():
    eng = create_engine(
        "sqlite+pysqlite:///:memory:", poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(eng, "connect")
    def _fk_on(dbapi_conn, _):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def db(engine):
    with Session(engine) as s:
        yield s


@pytest.fixture()
def artist(db):
    a = ArtistProfile(stage_name="Sam")
    db.add(a)
    db.commit()
    return a


def make_song(artist, slug, **kw):
    return Song(artist_id=artist.id, title=slug.title(), slug=slug, **kw)


def test_all_tables_created(engine):
    assert set(inspect(engine).get_table_names()) == EXPECTED_TABLES


def test_user_defaults_and_unique_email(db):
    u = User(name="A", email="a@example.com", password_hash="x")
    db.add(u)
    db.commit()
    assert u.role == UserRole.EDITOR and u.is_active is True
    db.add(User(name="B", email="a@example.com", password_hash="y"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_album_songs_ordered_and_standalone_single(db, artist):
    album = Album(artist_id=artist.id, title="First", slug="first")
    db.add(album)
    db.commit()
    db.add_all([
        make_song(artist, "b-side", album_id=album.id, track_number=2),
        make_song(artist, "a-side", album_id=album.id, track_number=1),
        make_song(artist, "single"),
    ])
    db.commit()
    db.refresh(album)
    assert [s.slug for s in album.songs] == ["a-side", "b-side"]
    single = db.scalar(select(Song).where(Song.slug == "single"))
    assert single.album_id is None


def test_song_defaults(db, artist):
    s = make_song(artist, "demo")
    db.add(s)
    db.commit()
    assert s.status == ContentStatus.DRAFT
    assert s.download_enabled is False
    assert s.play_count == 0 and s.download_count == 0
    assert s.created_at is not None


def test_foreign_key_enforced(db):
    db.add(Song(artist_id=9999, title="Ghost", slug="ghost"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_deleting_album_keeps_songs_as_singles(db, artist):
    album = Album(artist_id=artist.id, title="Gone", slug="gone")
    db.add(album)
    db.commit()
    song = make_song(artist, "kept", album_id=album.id, track_number=1)
    db.add(song)
    db.commit()
    db.delete(album)
    db.commit()
    db.refresh(song)
    assert song.album_id is None


def test_blog_tags_category_and_comment_cascade(db):
    cat = BlogCategory(name="News", slug="news")
    t1, t2 = BlogTag(name="Tour", slug="tour"), BlogTag(name="Studio", slug="studio")
    post = BlogPost(title="Hello", slug="hello", content="<p>Hi</p>", category=cat, tags=[t1, t2])
    db.add(post)
    db.commit()
    assert {t.slug for t in post.tags} == {"tour", "studio"}
    assert [p.slug for p in t1.posts] == ["hello"]

    c = Comment(post_id=post.id, name="Fan", email="f@example.com", body="Nice")
    db.add(c)
    db.commit()
    assert c.status == CommentStatus.PENDING  # moderation-first

    db.delete(post)
    db.commit()
    assert db.scalar(select(func.count()).select_from(Comment)) == 0
    assert db.scalar(select(func.count()).select_from(BlogTag)) == 2  # tags survive


def test_media_gallery_and_restrict_delete(db):
    m = MediaFile(kind=MediaKind.IMAGE, storage_key="images/ab12.jpg",
                  original_filename="x.jpg", mime_type="image/jpeg", size_bytes=1234)
    db.add(m)
    db.commit()
    g = GalleryItem(image_id=m.id, title="Stage")
    db.add(g)
    db.commit()
    assert g.image.storage_key == "images/ab12.jpg"
    db.delete(m)
    with pytest.raises(IntegrityError):
        db.commit()  # image still used by gallery item
    db.rollback()


def test_video_defaults(db, artist):
    v = Video(artist_id=artist.id, title="Clip", slug="clip", external_url="https://youtu.be/x")
    db.add(v)
    db.commit()
    assert v.view_count == 0 and v.status == ContentStatus.DRAFT


def test_analytics_events_and_cascade(db, artist):
    s = make_song(artist, "hit")
    db.add(s)
    db.commit()
    db.add_all([PlayEvent(song_id=s.id), DownloadEvent(song_id=s.id, ip_address="203.0.113.5")])
    db.commit()
    assert db.scalar(select(func.count()).select_from(PlayEvent)) == 1
    db.delete(s)
    db.commit()
    assert db.scalar(select(func.count()).select_from(PlayEvent)) == 0
    assert db.scalar(select(func.count()).select_from(DownloadEvent)) == 0


def test_video_view_event(db, artist):
    v = Video(artist_id=artist.id, title="V", slug="v")
    db.add(v)
    db.commit()
    db.add(VideoViewEvent(video_id=v.id))
    db.commit()
    assert db.scalar(select(func.count()).select_from(VideoViewEvent)) == 1


def test_contact_social_settings_audit(db):
    msg = ContactMessage(name="N", email="n@example.com", subject="Hi", message="Booking?")
    db.add_all([
        msg,
        SocialLink(platform="instagram", url="https://instagram.com/x"),
        SiteSetting(key="default_theme", value="dark", group="appearance"),
    ])
    u = User(name="Admin", email="adm@example.com", password_hash="x", role=UserRole.SUPER_ADMIN)
    db.add(u)
    db.commit()
    assert msg.is_read is False and msg.is_archived is False

    log = AuditLog(admin_id=u.id, action="album.create", entity_type="album",
                   entity_id=1, extra={"title": "First"})
    db.add(log)
    db.commit()
    assert log.extra == {"title": "First"}
    db.delete(u)
    db.commit()
    db.refresh(log)
    assert log.admin_id is None  # audit history survives user deletion


def test_site_setting_key_unique(db):
    db.add(SiteSetting(key="k", value=1))
    db.commit()
    db.add(SiteSetting(key="k", value=2))
    with pytest.raises(IntegrityError):
        db.commit()
