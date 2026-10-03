from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ContentStatus, VideoSource, VideoType
from app.models.mixins import TimestampMixin, enum_type


class Video(TimestampMixin, Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist_profiles.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200), index=True)
    slug: Mapped[str] = mapped_column(String(220), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    thumbnail_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    source_type: Mapped[VideoSource] = mapped_column(
        enum_type(VideoSource), default=VideoSource.EXTERNAL,
        server_default=VideoSource.EXTERNAL.name,
    )
    media_file_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    external_url: Mapped[str | None] = mapped_column(String(500))
    video_type: Mapped[VideoType] = mapped_column(
        enum_type(VideoType), default=VideoType.MUSIC_VIDEO,
        server_default=VideoType.MUSIC_VIDEO.name, index=True,
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    release_date: Mapped[date | None] = mapped_column(Date, index=True)
    status: Mapped[ContentStatus] = mapped_column(
        enum_type(ContentStatus), default=ContentStatus.DRAFT,
        server_default=ContentStatus.DRAFT.name, index=True,
    )
    view_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    artist = relationship("ArtistProfile", back_populates="videos")
    thumbnail = relationship("MediaFile", foreign_keys=[thumbnail_id])
    media_file = relationship("MediaFile", foreign_keys=[media_file_id])
