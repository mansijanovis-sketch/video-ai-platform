from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
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
        nullable=True,
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
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    detections = relationship(
        "Detection",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    transcript_segments = relationship(
        "TranscriptSegment",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    tutorial_steps = relationship(
        "TutorialStep",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    evidence = relationship(
        "VideoEvidence",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    youtube_url = Column(
        String,
        nullable=True,
    )

    youtube_video_id = Column(
        String,
        nullable=True,
        index=True,
    )

    source_type = Column(
        String,
        nullable=False,
        default="upload",
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

    x1 = Column(
        Float,
        nullable=False,
    )

    y1 = Column(
        Float,
        nullable=False,
    )

    x2 = Column(
        Float,
        nullable=False,
    )

    y2 = Column(
        Float,
        nullable=False,
    )

    video = relationship(
        "Video",
        back_populates="detections",
    )


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

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

    start_time = Column(
        Float,
        nullable=False,
    )

    end_time = Column(
        Float,
        nullable=False,
    )

    text = Column(
        Text,
        nullable=False,
    )

    video = relationship(
        "Video",
        back_populates="transcript_segments",
    )

class TutorialStep(Base):
    __tablename__ = "tutorial_steps"

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

    step_number = Column(
        Integer,
        nullable=False,
    )

    action = Column(
        String,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    verified = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    name = Column(
        String,
        nullable=True,
    )

    path = Column(
        String,
        nullable=True,
    )

    instruction = Column(
        Text,
        nullable=False,
    )

    start_time = Column(
        Float,
        nullable=False,
    )

    end_time = Column(
        Float,
        nullable=False,
    )

    evidence_source = Column(
        String,
        nullable=False,
    )

    evidence_text = Column(
        Text,
        nullable=False,
    )

    video = relationship(
        "Video",
        back_populates="tutorial_steps",
    )


class VideoEvidence(Base):
    __tablename__ = "video_evidence"

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

    evidence_type = Column(
        String,
        nullable=False,
    )

    text = Column(
        Text,
        nullable=False,
    )

    source = Column(
        String,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    video = relationship(
        "Video",
        back_populates="evidence",
    )


class EarlyAccessSignup(Base):
    __tablename__ = "early_access_signups"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )