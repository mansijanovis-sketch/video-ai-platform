import os
import shutil
import uuid
import logging

from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from ..config import UPLOAD_DIR
from ..database import get_db
from ..models import Video, Detection
from ..services.video_processor import get_video_info
from ..services.analyzer import analyze_video
from ..services.analysis_job import run_analysis_job
from ..services.video_url import acquire_video_from_url
from ..services.youtube import extract_youtube_video_id
from .youtube import populate_youtube_analysis


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)

logger = logging.getLogger(__name__)



os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


# ==================================================
# Upload Video
# ==================================================

@router.post("/upload")
def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    allowed_extensions = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
    }

    original_filename = Path(file.filename).name
    extension = Path(original_filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported video format. "
                "Allowed formats: "
                + ", ".join(sorted(allowed_extensions))
            ),
        )

    unique_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        unique_filename,
    )

    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        info = get_video_info(filepath)

    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)

        logger.exception("Unable to process uploaded video")

        raise HTTPException(
            status_code=400,
            detail="Invalid video file.",
        )

    video = Video(
        filename=original_filename,
        filepath=filepath,
        duration=info["duration"],
        fps=info["fps"],
        status="uploaded",
        source_type="upload",
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return {
        "id": video.id,
        "filename": video.filename,
        "filepath": video.filepath,
        "duration": video.duration,
        "fps": video.fps,
        "status": video.status,
    }

# ==================================================
# Analyze Video
# ==================================================

@router.post("/{video_id}/analyze")
def analyze_uploaded_video(
    video_id: int,
    background_tasks: BackgroundTasks,
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

    if video.status == "processing":
        raise HTTPException(
            status_code=409,
            detail="Video analysis is already in progress.",
        )

    video.status = "processing"
    db.commit()

    background_tasks.add_task(
        run_analysis_job,
        video.id,
    )

    return {
        "video_id": video.id,
        "status": "processing",
        "message": "Video analysis started.",
    }

# ==================================================
# Add Video From URL
# ==================================================

def _youtube_response(video: Video, message: str):
    return {
        "id": video.id,
        "youtube_url": video.youtube_url,
        "youtube_video_id": video.youtube_video_id,
        "source_type": video.source_type,
        "status": video.status,
        "message": message,
    }


def _add_youtube_video_from_transcript(
    url: str,
    youtube_video_id: str,
    db: Session,
):
    existing_video = (
        db.query(Video)
        .filter(Video.youtube_video_id == youtube_video_id)
        .first()
    )

    if existing_video:
        if existing_video.status != "completed":
            try:
                existing_video.status = "processing"
                db.commit()
                populate_youtube_analysis(db, existing_video)
            except Exception:
                logger.exception(
                    "YouTube transcript analysis failed for video %s",
                    existing_video.id,
                )
                db.rollback()
                existing_video = db.query(Video).filter(
                    Video.id == existing_video.id
                ).first()
                if existing_video:
                    existing_video.status = "failed"
                    db.commit()
                raise HTTPException(
                    status_code=422,
                    detail="Unable to analyze this YouTube tutorial.",
                )

        return _youtube_response(
            existing_video,
            "This YouTube video already exists.",
        )

    video = Video(
        filename=f"youtube_{youtube_video_id}",
        filepath=None,
        duration=0,
        fps=0,
        status="uploaded",
        youtube_url=url,
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
    except Exception:
        logger.exception(
            "YouTube transcript analysis failed for video %s",
            video.id,
        )
        db.rollback()
        video = db.query(Video).filter(
            Video.id == video.id
        ).first()
        if video:
            video.status = "failed"
            db.commit()
        raise HTTPException(
            status_code=422,
            detail="Unable to analyze this YouTube tutorial.",
        )

    return _youtube_response(
        video,
        "YouTube video added successfully.",
    )

@router.post("/url")
def add_video_from_url(
    url: str,
    db: Session = Depends(get_db),
):
    url = url.strip()

    if not url:
        raise HTTPException(
            status_code=400,
            detail="A video URL is required.",
        )

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only HTTP and HTTPS URLs are supported.",
        )

    youtube_video_id = extract_youtube_video_id(url)
    if youtube_video_id:
        return _add_youtube_video_from_transcript(
            url=url,
            youtube_video_id=youtube_video_id,
            db=db,
        )

    try:
        result = acquire_video_from_url(
            url
        )

        filepath = result["filepath"]

        if not os.path.exists(filepath):
            raise ValueError(
                "Video acquisition completed, "
                "but the video file was not found."
            )

        info = get_video_info(
            filepath
        )

    except Exception:

        if "filepath" in locals():
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass

        logger.exception("Unable to acquire video from URL")
        raise HTTPException(
            status_code=400,
            detail="Unable to acquire video from URL.",
        )

    source_type = result.get(
        "source_type",
        "url",
    )

    video = Video(
        filename=(
            result.get("title")
            or Path(filepath).name
        ),
        filepath=filepath,
        duration=(
            info.get("duration")
            or result.get("duration")
            or 0
        ),
        fps=(
            info.get("fps")
            or result.get("fps")
            or 0
        ),
        status="uploaded",
        source_type=source_type,
        youtube_url=(
            url
            if source_type == "youtube"
            else None
        ),
        youtube_video_id=(
            result.get("external_id")
            if source_type == "youtube"
            else None
        ),
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return {
        "id": video.id,
        "filename": video.filename,
        "filepath": video.filepath,
        "duration": video.duration,
        "fps": video.fps,
        "status": video.status,
        "source_type": video.source_type,
        "youtube_url": video.youtube_url,
        "youtube_video_id": video.youtube_video_id,
        "message": "Video added successfully.",
    }

# ==================================================
# Get Video Detections
# ==================================================

@router.get("/{video_id}/detections")
def get_video_detections(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(
        Video.id == video_id
    ).first()

    if not video:
        return {
            "error": "Video not found"
        }

    detections = []

    for detection in video.detections:

        detections.append(
            {
                "id": detection.id,
                "timestamp": detection.timestamp,
                "label": detection.label,
                "confidence": detection.confidence,
                "x1": detection.x1,
                "y1": detection.y1,
                "x2": detection.x2,
                "y2": detection.y2,
            }
        )

    return {
        "video_id": video.id,
        "detections": detections,
    }


# ==================================================
# Get Video Details
# ==================================================

@router.get("/{video_id}")
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(
        Video.id == video_id
    ).first()

    if not video:
        return {
            "error": "Video not found"
        }

    return {
        "id": video.id,
        "filename": video.filename,
        "filepath": video.filepath,
        "duration": video.duration,
        "fps": video.fps,
        "status": video.status,
        "description": video.description,
        "source_type": video.source_type,
        "youtube_url": video.youtube_url,
        "youtube_video_id": video.youtube_video_id,
        "created_at": video.created_at,
    }
