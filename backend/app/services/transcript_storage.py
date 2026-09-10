from sqlalchemy.orm import Session

from ..models import TranscriptSegment


def save_transcript(
    db: Session,
    video_id: int,
    segments: list[dict],
):
    db.query(TranscriptSegment).filter(
        TranscriptSegment.video_id == video_id
    ).delete(
        synchronize_session=False
    )

    saved_segments = []

    for segment in segments:
        transcript_segment = TranscriptSegment(
            video_id=video_id,
            start_time=segment["start_time"],
            end_time=segment["end_time"],
            text=segment["text"],
        )

        db.add(transcript_segment)
        saved_segments.append(
            transcript_segment
        )

    db.commit()

    return saved_segments