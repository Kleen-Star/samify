from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base import Base
from app.models.enums import ContentStatus
from app.models.mixins import TimestampMixin, enum_type


class Album(TimestampMixin, Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist_profiles.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(220), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    genre: Mapped[str | None] = mapped_column(String(100))
    release_date: Mapped[date | None] = mapped_column(Date)
    cover_image_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    status: Mapped[ContentStatus] = mapped_column(
        enum_type(ContentStatus), default=ContentStatus.DRAFT,
        server_default=ContentStatus.DRAFT.name, index=True,
    )

    artist = relationship("ArtistProfile", back_populates="albums")
    cover_image = relationship("MediaFile", foreign_keys=[cover_image_id])
    songs = relationship(
        "Song", back_populates="album", order_by="Song.track_number", passive_deletes=True
    )


class Song(TimestampMixin, Base):
    __tablename__ = "songs"
    __table_args__ = (Index("ix_songs_album_track", "album_id", "track_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist_profiles.id", ondelete="CASCADE"), index=True
    )
    album_id: Mapped[int | None] = mapped_column(ForeignKey("albums.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(220), unique=True)
    featured_artists: Mapped[list | None] = mapped_column(JSON)
    genre: Mapped[str | None] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    cover_image_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    audio_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    track_number: Mapped[int | None] = mapped_column(Integer)
    release_date: Mapped[date | None] = mapped_column(Date, index=True)
    download_enabled: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false()
    )
    status: Mapped[ContentStatus] = mapped_column(
        enum_type(ContentStatus), default=ContentStatus.DRAFT,
        server_default=ContentStatus.DRAFT.name, index=True,
    )
    # Denormalised counters; the event tables are the source of truth
    play_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    download_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    artist = relationship("ArtistProfile", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    cover_image = relationship("MediaFile", foreign_keys=[cover_image_id])
    audio_file = relationship("MediaFile", foreign_keys=[audio_file_id])
