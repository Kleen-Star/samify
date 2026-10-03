from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class ArtistProfile(TimestampMixin, Base):
    __tablename__ = "artist_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    stage_name: Mapped[str] = mapped_column(String(150))
    real_name: Mapped[str | None] = mapped_column(String(150))
    tagline: Mapped[str | None] = mapped_column(String(255))
    short_intro: Mapped[str | None] = mapped_column(Text)
    biography: Mapped[str | None] = mapped_column(Text)
    career_history: Mapped[str | None] = mapped_column(Text)
    genre: Mapped[str | None] = mapped_column(String(120))
    achievements: Mapped[list | None] = mapped_column(JSON)
    awards: Mapped[list | None] = mapped_column(JSON)
    milestones: Mapped[list | None] = mapped_column(JSON)
    profile_image_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    hero_image_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )

    albums = relationship("Album", back_populates="artist", passive_deletes=True)
    songs = relationship("Song", back_populates="artist", passive_deletes=True)
    videos = relationship("Video", back_populates="artist", passive_deletes=True)
