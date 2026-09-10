from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Video
from ..services.transcript_search import search_transcript


router = APIRouter(
    prefix="/videos",
    tags=["ask"],
)


@router.post("/{video_id}/ask")
def ask_video(
    video_id: int,
    question: str,
    db: Session = Depends(get_db),
):
    # -------------------------------------------------
    # Check that the video exists
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Validate question
    # -------------------------------------------------

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    # -------------------------------------------------
    # Search transcript
    # -------------------------------------------------

    results = search_transcript(
        db=db,
        video_id=video_id,
        question=question,
        limit=5,
    )

    # -------------------------------------------------
    # No relevant result
    # -------------------------------------------------

    if not results:
        return {
            "video_id": video_id,
            "question": question,
            "answer": (
                "I could not find a relevant "
                "section in the video."
            ),
            "timestamp": None,
            "evidence": None,
        }

    # -------------------------------------------------
    # Use best result
    # -------------------------------------------------

    best_result = results[0]

    start_time = best_result[
        "start_time"
    ]

    end_time = best_result[
        "end_time"
    ]

    evidence_text = best_result[
        "text"
    ]

    # -------------------------------------------------
    # Build initial answer
    # -------------------------------------------------

    answer = (
        "The most relevant section of the "
        "tutorial is between "
        f"{start_time:.2f}s and "
        f"{end_time:.2f}s."
    )

    return {
        "video_id": video_id,
        "question": question,
        "answer": answer,
        "timestamp": {
            "start": start_time,
            "end": end_time,
        },
        "evidence": {
            "source": "transcript",
            "text": evidence_text,
        },
        "score": best_result[
            "score"
        ],
    }