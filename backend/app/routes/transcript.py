from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    Video,
    TranscriptSegment,
    TutorialStep,
    VideoEvidence,
)

router = APIRouter(
    prefix="/videos",
    tags=["tutorial"],
)


@router.get("/{video_id}/transcript")
def get_transcript(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found",
        )

    segments = (
        db.query(TranscriptSegment)
        .filter(
            TranscriptSegment.video_id == video_id
        )
        .order_by(
            TranscriptSegment.start_time
        )
        .all()
    )

    return {
        "video_id": video_id,
        "filename": video.filename,
        "segments": [
            {
                "id": segment.id,
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "text": segment.text,
            }
            for segment in segments
        ],
    }


@router.get("/{video_id}/steps")
def get_tutorial_steps(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found",
        )

    steps = (
        db.query(TutorialStep)
        .filter(
            TutorialStep.video_id == video_id
        )
        .order_by(
            TutorialStep.step_number
        )
        .all()
    )

    return {
        "video_id": video_id,
        "filename": video.filename,
        "steps": [
            {
                "id": step.id,
                "step": step.step_number,
                "action": step.action,
		"confidence": step.confidence,
		"verified": step.verified,
		"name": step.name,
		"path": step.path,
                "instruction": step.instruction,
                "start_time": step.start_time,
                "end_time": step.end_time,
                "evidence": {
                    "source": step.evidence_source,
                    "text": step.evidence_text,
                },
            }
            for step in steps
        ],
    }

@router.get("/{video_id}/evidence")
def get_video_evidence(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = (
        db.query(Video)
        .filter(
            Video.id == video_id
        )
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found",
        )

    evidence = (
        db.query(VideoEvidence)
        .filter(
            VideoEvidence.video_id == video_id
        )
        .order_by(
            VideoEvidence.timestamp
        )
        .all()
    )

    return {
        "video_id": video_id,
        "filename": video.filename,
        "evidence": [
            {
                "id": item.id,
                "timestamp": item.timestamp,
                "evidence_type": item.evidence_type,
                "text": item.text,
                "source": item.source,
                "confidence": item.confidence,
            }
            for item in evidence
        ],
    }