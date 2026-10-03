from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum as SAEnum, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

# BIGINT primary keys that still autoincrement on SQLite (used by tests)
BigPK = BigInteger().with_variant(Integer, "sqlite")


def enum_type(enum_cls):
    """Store enums as VARCHAR (no native ENUM) so migrations stay simple."""
    return SAEnum(enum_cls, native_enum=False, length=30)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
