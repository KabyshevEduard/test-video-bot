from sqlalchemy import func
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Video(Base):
    __tablename__ = 'videos'

    index: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement='auto')
    video_created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    creator_id: Mapped[str] = mapped_column(String(500))

    def __repr__(self):
        return f'Video(id={self.index})'


class Snapshot(Base):
    __tablename__ = 'snapshots'

    index: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement='auto')
    video_id: Mapped[Optional[int]] = mapped_column(ForeignKey('videos.index'))
    views_count: Mapped[int] = mapped_column(Integer)
    likes_count: Mapped[int] = mapped_column(Integer)
    reports_count: Mapped[int] = mapped_column(Integer)
    comments_count: Mapped[int] = mapped_column(Integer)
    delta_views_count: Mapped[int] = mapped_column(Integer)
    delta_likes_count: Mapped[int] = mapped_column(Integer)
    delta_reports_count: Mapped[int] = mapped_column(Integer)
    delta_comments_count: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f'Snapshot(id={self.index})'