import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Video
from ..services.youtube import (
    extract_youtube_video_id,
)
from ..services.youtube_transcript import (
    TranscriptAccessBlockedError,
    TranscriptUnavailableError,
    YouTubeTranscriptError,
    fetch_youtube_transcript,
)
from ..services.youtube_transcript_cleaner import (
    clean_youtube_segments,
)
from ..services.youtube_transcript_storage import (
    save_youtube_transcript,
)
from ..services.developer_action_pipeline import (
    build_tutorial_steps,
)
from ..services.tutorial_step_storage import (
    save_tutorial_steps,
)


router = APIRouter(
    prefix="/videos",
    tags=["youtube"],
)

logger = logging.getLogger(__name__)


def transcript_http_error(error: YouTubeTranscriptError):
    if isinstance(error, TranscriptUnavailableError):
        return HTTPException(
            status_code=422,
            detail="No transcript is available for this YouTube video.",
        )

    if isinstance(error, TranscriptAccessBlockedError):
        return HTTPException(
            status_code=503,
            detail=(
                "YouTube transcript access is temporarily unavailable "
                "from the production server."
            ),
        )

    return HTTPException(
        status_code=503,
        detail="The YouTube transcript provider is temporarily unavailable.",
    )


def populate_youtube_analysis(
    db: Session,
    video: Video,
):
    transcript = fetch_youtube_transcript(
        video.youtube_video_id
    )
    segments = clean_youtube_segments(
        transcript.get("segments", [])
    )

    if not segments:
        raise ValueError(
            "No transcript was available for this YouTube video."
        )

    save_youtube_transcript(
        db=db,
        video_id=video.id,
        segments=segments,
    )

    steps = build_tutorial_steps(segments)
    save_tutorial_steps(
        db=db,
        video_id=video.id,
        steps=steps,
    )

    video.status = "completed"
    db.commit()


@router.post("/youtube")
def create_youtube_video(
    url: str,
    db: Session = Depends(get_db),
):
    youtube_video_id = (
        extract_youtube_video_id(url)
    )

    if not youtube_video_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL.",
        )

    existing_video = (
        db.query(Video)
        .filter(
            Video.youtube_video_id
            == youtube_video_id
        )
        .first()
    )

    if existing_video:
        if existing_video.status != "completed":
            try:
                existing_video.status = "processing"
                db.commit()
                populate_youtube_analysis(
                    db,
                    existing_video,
                )
            except Exception as error:
                logger.exception(
                    "YouTube analysis failed for video %s",
                    existing_video.id,
                )
                db.rollback()
                existing_video = db.query(Video).filter(
                    Video.id == existing_video.id
                ).first()
                if existing_video:
                    existing_video.status = "failed"
                    db.commit()
                if isinstance(error, YouTubeTranscriptError):
                    raise transcript_http_error(error) from error
                raise HTTPException(
                    status_code=422,
                    detail="Unable to analyze this YouTube tutorial.",
                ) from error

        return {
            "id": existing_video.id,
            "youtube_url": existing_video.youtube_url,
            "youtube_video_id": (
                existing_video.youtube_video_id
            ),
            "source_type": (
                existing_video.source_type
            ),
            "status": existing_video.status,
            "message": (
                "This YouTube video "
                "already exists."
            ),
        }

    video = Video(
        filename=(
            f"youtube_{youtube_video_id}"
        ),
        filepath=None,
        duration=0,
        fps=0,
        status="uploaded",
        youtube_url=url.strip(),
        youtube_video_id=youtube_video_id,
        source_type="youtube",
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    try:
        video.status = "processing"
        db.commit()
        populate_youtube_analysis(db, video)
    except Exception as error:
        logger.exception(
            "YouTube analysis failed for video %s",
            video.id,
        )
        db.rollback()
        video = db.query(Video).filter(
            Video.id == video.id
        ).first()
        if video:
            video.status = "failed"
            db.commit()
        if isinstance(error, YouTubeTranscriptError):
            raise transcript_http_error(error) from error
        raise HTTPException(
            status_code=422,
            detail="Unable to analyze this YouTube tutorial.",
        ) from error

    return {
        "id": video.id,
        "youtube_url": video.youtube_url,
        "youtube_video_id": (
            video.youtube_video_id
        ),
        "source_type": video.source_type,
        "status": video.status,
        "message": (
            "YouTube video added "
            "successfully."
        ),
    }