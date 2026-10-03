from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import UserRole
from app.models.mixins import TimestampMixin, enum_type


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        enum_type(UserRole), default=UserRole.EDITOR, server_default=UserRole.EDITOR.name
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime)
