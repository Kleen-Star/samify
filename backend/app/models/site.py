from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from app.db.base import Base
from app.models.mixins import TimestampMixin


class SocialLink(TimestampMixin, Base):
    __tablename__ = "social_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    artist_id: Mapped[int | None] = mapped_column(
        ForeignKey("artist_profiles.id", ondelete="CASCADE"), index=True
    )  # NULL = site-wide link
    platform: Mapped[str] = mapped_column(String(50))
    label: Mapped[str | None] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true()
    )


class SiteSetting(TimestampMixin, Base):
    """Key/value site configuration (site name, default theme, comment rules, ...)."""

    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True)
    value = mapped_column(JSON, nullable=True)
    group: Mapped[str | None] = mapped_column(String(50), index=True)
