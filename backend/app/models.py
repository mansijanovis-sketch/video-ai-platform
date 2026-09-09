from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from .database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    filepath = Column(
        String,
        nullable=False,
    )

    duration = Column(
        Float,
        nullable=True,
    )

    fps = Column(
        Float,
        nullable=True,
    )

    status = Column(
        String,
        default="uploaded",
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    detections = relationship(
        "Detection",
        back_populates="video",
        cascade="all, delete-orphan",
    )


class Detection(Base):
    __tablename__ = "detections"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    video_id = Column(
        Integer,
        ForeignKey("videos.id"),
        nullable=False,
    )

    timestamp = Column(
        Float,
        nullable=False,
    )

    label = Column(
        String,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
    )

    x1 = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)

    video = relationship(
        "Video",
        back_populates="detections",
    )