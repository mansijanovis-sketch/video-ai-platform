import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Video, Detection
from ..services.video_processor import get_video_info
from ..services.analyzer import analyze_video


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


UPLOAD_DIR = "uploads"

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
    filename = file.filename

    filepath = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    with open(
        filepath,
        "wb",
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer,
        )

    info = get_video_info(
        filepath
    )

    video = Video(
        filename=filename,
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
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(
        Video.id == video_id
    ).first()

    if not video:
        return {
            "error": "Video not found"
        }

    # Remove previous detections
    db.query(Detection).filter(
        Detection.video_id == video.id
    ).delete(
        synchronize_session=False
    )

    video.status = "processing"

    db.commit()

    try:

        result = analyze_video(
            video_path=video.filepath,
            video_id=video.id,
            db=db,
            video_duration=video.duration or 0,
        )

        video.description = result[
            "description"
        ]

        video.status = "completed"

        db.commit()

        return {
            "video_id": video.id,
            "status": video.status,
            "frames_processed": result[
                "frames_processed"
            ],
            "detections_created": result[
                "detections_created"
            ],
            "description": result[
                "description"
            ],
            "ocr_results": result[
                "ocr_results"
            ],
            "object_summary": result["object_summary"],
            "scene_changes": result["scene_changes"],
            "timeline": result["timeline"],
        }

    except Exception as e:

        video.status = "failed"

        db.commit()

        return {
            "video_id": video.id,
            "status": "failed",
            "error": str(e),
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
