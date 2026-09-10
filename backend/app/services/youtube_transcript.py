from youtube_transcript_api import (
    YouTubeTranscriptApi,
)


def fetch_youtube_transcript(
    video_id: str,
):
    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=["en"],
    )

    segments = []

    for snippet in transcript:

        start_time = float(
            snippet.start
        )

        duration = float(
            snippet.duration
        )

        end_time = (
            start_time + duration
        )

        text = snippet.text.strip()

        if not text:
            continue

        segments.append(
            {
                "start_time": start_time,
                "end_time": end_time,
                "text": text,
            }
        )

    return {
        "video_id": video_id,
        "language": transcript.language,
        "language_code": transcript.language_code,
        "is_generated": transcript.is_generated,
        "segments": segments,
    }