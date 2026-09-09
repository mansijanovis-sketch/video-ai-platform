from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Video, Detection
from .analyzer import analyze_video


def run_analysis_job(video_id: int):
    db: Session = SessionLocal()

    try:
        video = (
            db.query(Video)
            .filter(Video.id == video_id)
            .first()
        )

        if not video:
            return

        video.status = "processing"
        db.commit()

        db.query(Detection).filter(
            Detection.video_id == video.id
        ).delete(
            synchronize_session=False
        )

        db.commit()

        result = analyze_video(
            video_path=video.filepath,
            video_id=video.id,
            db=db,
            video_duration=video.duration or 0,
        )

        video.description = result["description"]
        video.status = "completed"

        db.commit()

    except Exception:
        db.rollback()

        video = (
            db.query(Video)
            .filter(Video.id == video_id)
            .first()
        )

        if video:
            video.status = "failed"
            db.commit()

    finally:
        db.close()