import logging

import requests
from youtube_transcript_api import (
    CouldNotRetrieveTranscript,
    IpBlocked,
    NoTranscriptFound,
    RequestBlocked,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

from ..config import (
    SUPADATA_API_KEY,
    SUPADATA_TIMEOUT_SECONDS,
)


logger = logging.getLogger(__name__)


class YouTubeTranscriptError(Exception):
    """Base error for transcript provider failures."""


class TranscriptUnavailableError(YouTubeTranscriptError):
    """The video has no usable transcript."""


class TranscriptAccessBlockedError(YouTubeTranscriptError):
    """The provider could not access the video from this server."""


class TranscriptProviderError(YouTubeTranscriptError):
    """The configured transcript provider failed."""


def _normalize_segments(
    video_id: str,
    language: str,
    language_code: str,
    is_generated: bool,
    segments: list[dict],
):
    normalized_segments = []

    for segment in segments:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue

        normalized_segments.append(
            {
                "start_time": float(segment["start_time"]),
                "end_time": float(segment["end_time"]),
                "text": text,
            }
        )

    return {
        "video_id": video_id,
        "language": language,
        "language_code": language_code,
        "is_generated": is_generated,
        "segments": normalized_segments,
    }


def _fetch_with_supadata(video_id: str):
    try:
        response = requests.get(
            "https://api.supadata.ai/v1/transcript",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "lang": "en",
                "text": "false",
                "mode": "native",
            },
            headers={
                "x-api-key": SUPADATA_API_KEY,
            },
            timeout=SUPADATA_TIMEOUT_SECONDS,
        )
    except requests.RequestException as error:
        raise TranscriptProviderError(
            "Transcript provider request failed."
        ) from error

    try:
        payload = response.json()
    except ValueError as error:
        raise TranscriptProviderError(
            "Transcript provider returned invalid data."
        ) from error

    error_code = payload.get("error")
    if response.status_code == 403 or error_code == "forbidden":
        raise TranscriptAccessBlockedError(
            "Transcript provider could not access the YouTube video."
        )

    if response.status_code == 401 or error_code == "unauthorized":
        raise TranscriptProviderError(
            "Transcript provider authentication failed."
        )

    if response.status_code == 206 or error_code == "transcript-unavailable":
        raise TranscriptUnavailableError(
            "No transcript is available for this YouTube video."
        )

    if response.status_code >= 400:
        raise TranscriptProviderError(
            "Transcript provider request failed."
        )

    content = payload.get("content")
    if not isinstance(content, list):
        raise TranscriptUnavailableError(
            "No timestamped transcript is available for this YouTube video."
        )

    segments = [
        {
            "start_time": float(chunk.get("offset", 0)) / 1000,
            "end_time": (
                float(chunk.get("offset", 0))
                + float(chunk.get("duration", 0))
            ) / 1000,
            "text": chunk.get("text", ""),
        }
        for chunk in content
    ]

    return _normalize_segments(
        video_id=video_id,
        language=payload.get("lang", "en"),
        language_code=payload.get("lang", "en"),
        is_generated=False,
        segments=segments,
    )


def _fetch_with_local_library(video_id: str):
    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(
            video_id,
            languages=["en"],
        )
    except (NoTranscriptFound, TranscriptsDisabled) as error:
        raise TranscriptUnavailableError(
            "No transcript is available for this YouTube video."
        ) from error
    except (IpBlocked, RequestBlocked) as error:
        raise TranscriptAccessBlockedError(
            "YouTube transcript access is blocked from this server."
        ) from error
    except CouldNotRetrieveTranscript as error:
        raise TranscriptProviderError(
            "The local transcript provider could not retrieve the transcript."
        ) from error

    segments = [
        {
            "start_time": float(snippet.start),
            "end_time": float(snippet.start) + float(snippet.duration),
            "text": snippet.text,
        }
        for snippet in transcript
    ]

    return _normalize_segments(
        video_id=video_id,
        language=transcript.language,
        language_code=transcript.language_code,
        is_generated=transcript.is_generated,
        segments=segments,
    )


def fetch_youtube_transcript(
    video_id: str,
):
    if SUPADATA_API_KEY:
        return _fetch_with_supadata(video_id)

    logger.warning(
        "SUPADATA_API_KEY is not configured; using the local transcript provider"
    )
    return _fetch_with_local_library(video_id)