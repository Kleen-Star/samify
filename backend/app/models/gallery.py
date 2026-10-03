from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ContentStatus
from app.models.mixins import TimestampMixin, enum_type


class GalleryItem(TimestampMixin, Base):
    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int | None] = mapped_column(
        ForeignKey("artist_profiles.id", ondelete="CASCADE"), index=True
    )
    image_id: Mapped[int] = mapped_column(ForeignKey("media_files.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    taken_on: Mapped[date | None] = mapped_column(Date)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    status: Mapped[ContentStatus] = mapped_column(
        enum_type(ContentStatus), default=ContentStatus.DRAFT,
        server_default=ContentStatus.DRAFT.name, index=True,
    )

    image = relationship("MediaFile", foreign_keys=[image_id])
