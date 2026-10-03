from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text,
)
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base import Base
from app.models.enums import CommentStatus, ContentStatus
from app.models.mixins import TimestampMixin, enum_type

LongText = Text().with_variant(mysql.MEDIUMTEXT(), "mysql")

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("blog_posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
)


class BlogCategory(TimestampMixin, Base):
    __tablename__ = "blog_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    posts = relationship("BlogPost", back_populates="category", passive_deletes=True)


class BlogTag(TimestampMixin, Base):
    __tablename__ = "blog_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)

    posts = relationship("BlogPost", secondary=post_tags, back_populates="tags")


class BlogPost(TimestampMixin, Base):
    __tablename__ = "blog_posts"
    __table_args__ = (Index("ix_blog_posts_status_published", "status", "published_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(280), unique=True)
    content: Mapped[str] = mapped_column(LongText)
    excerpt: Mapped[str | None] = mapped_column(Text)
    featured_image_id: Mapped[int | None] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL")
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("blog_categories.id", ondelete="SET NULL"), index=True
    )
    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    status: Mapped[ContentStatus] = mapped_column(
        enum_type(ContentStatus), default=ContentStatus.DRAFT,
        server_default=ContentStatus.DRAFT.name,
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    comments_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true()
    )
    view_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    category = relationship("BlogCategory", back_populates="posts")
    author = relationship("User")
    featured_image = relationship("MediaFile", foreign_keys=[featured_image_id])
    tags = relationship("BlogTag", secondary=post_tags, back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan", passive_deletes=True
    )


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"
    __table_args__ = (Index("ix_comments_post_status", "post_id", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[CommentStatus] = mapped_column(
        enum_type(CommentStatus), default=CommentStatus.PENDING,
        server_default=CommentStatus.PENDING.name, index=True,
    )
    ip_hash: Mapped[str | None] = mapped_column(String(64))  # hashed, never the raw IP
    moderated_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    post = relationship("BlogPost", back_populates="comments")
