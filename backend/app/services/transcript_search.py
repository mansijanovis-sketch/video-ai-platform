import re

from sqlalchemy.orm import Session

from ..models import TranscriptSegment


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "be",
    "does",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "the",
    "this",
    "to",
    "was",
    "what",
    "where",
    "which",
    "who",
    "with",
}


def normalize_text(text: str) -> str:
    """
    Convert text to lowercase and remove punctuation.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s_.-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


def extract_keywords(text: str) -> list[str]:
    """
    Extract meaningful keywords from text.
    """

    normalized = normalize_text(text)

    words = normalized.split()

    keywords = []

    for word in words:
        if word in STOP_WORDS:
            continue

        if len(word) < 2:
            continue

        keywords.append(word)

    return keywords


def calculate_score(
    question: str,
    transcript_text: str,
) -> float:
    """
    Calculate a simple relevance score between
    a question and a transcript segment.
    """

    question_normalized = normalize_text(
        question
    )

    transcript_normalized = normalize_text(
        transcript_text
    )

    question_keywords = extract_keywords(
        question
    )

    if not question_keywords:
        return 0.0

    transcript_words = set(
        transcript_normalized.split()
    )

    matched_keywords = 0

    for keyword in question_keywords:
        if keyword in transcript_words:
            matched_keywords += 1

    keyword_score = (
        matched_keywords
        / len(question_keywords)
    )

    phrase_score = 0.0

    if (
        question_normalized
        and question_normalized
        in transcript_normalized
    ):
        phrase_score = 1.0

    score = (
        keyword_score * 0.8
        + phrase_score * 0.2
    )

    return round(
        score,
        4,
    )


def search_transcript(
    db: Session,
    video_id: int,
    question: str,
    limit: int = 5,
) -> list[dict]:
    """
    Search transcript segments for the most
    relevant segments to the user's question.
    """

    if not question.strip():
        return []

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

    results = []

    for segment in segments:

        score = calculate_score(
            question=question,
            transcript_text=segment.text,
        )

        if score < 0.3:
            continue

        results.append(
            {
                "segment_id": segment.id,
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "text": segment.text,
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:limit]