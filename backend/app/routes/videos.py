import os
import shutil
import uuid

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


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)



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

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)

        raise HTTPException(
            status_code=400,
            detail=f"Invalid video file: {str(e)}",
        )

    video = Video(
        filename=original_filename,
        filepath=filepath,
        duration=info["duration"],
        fps=info["fps"],
        status="uploaded",
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
        "created_at": video.created_at,
    }
