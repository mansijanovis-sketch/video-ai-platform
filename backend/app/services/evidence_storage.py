from sqlalchemy.orm import Session

from ..models import VideoEvidence


def save_video_evidence(
    db: Session,
    video_id: int,
    evidence: list[dict],
):
    db.query(VideoEvidence).filter(
        VideoEvidence.video_id == video_id
    ).delete(
        synchronize_session=False
    )

    saved_evidence = []

    for item in evidence:
        text = item.get(
            "text",
            "",
        ).strip()

        if not text:
            continue

        video_evidence = VideoEvidence(
            video_id=video_id,
            timestamp=float(
                item.get(
                    "timestamp",
                    0.0,
                )
            ),
            evidence_type=item.get(
                "evidence_type",
                "ocr",
            ),
            text=text,
            source=item.get(
                "source",
                "video_frame",
            ),
            confidence=float(
                item.get(
                    "confidence",
                    0.0,
                )
            ),
        )

        db.add(video_evidence)
        saved_evidence.append(
            video_evidence
        )

    db.commit()

    return saved_evidence