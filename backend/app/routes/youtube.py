from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Video
from ..services.youtube import (
    extract_youtube_video_id,
)


router = APIRouter(
    prefix="/videos",
    tags=["youtube"],
)


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