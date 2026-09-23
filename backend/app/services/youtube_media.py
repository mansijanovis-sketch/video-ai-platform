from __future__ import annotations

import os

import yt_dlp

from ..config import UPLOAD_DIR


def get_youtube_video_info(
    youtube_url: str,
) -> dict:
    """
    Fetch YouTube metadata without downloading media.
    """

    options = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            youtube_url,
            download=False,
        )

    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "duration": info.get("duration"),
        "width": info.get("width"),
        "height": info.get("height"),
        "fps": info.get("fps"),
        "ext": info.get("ext"),
    }


def download_youtube_video(
    youtube_url: str,
    output_dir: str | None = None,
) -> dict:
    """
    Download a video-only H.264 MP4 stream suitable
    for OpenCV frame extraction.

    The downloaded file is intentionally kept separate
    from the existing upload pipeline.
    """

    output_dir = output_dir or os.path.join(UPLOAD_DIR, "youtube")

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    options = {
        "format": "311",
        "outtmpl": os.path.join(
            output_dir,
            "%(id)s.%(ext)s",
        ),
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(options) as ydl:

        info = ydl.extract_info(
            youtube_url,
            download=True,
        )

    filepath = os.path.join(
        output_dir,
        f"{info['id']}.{info['ext']}",
    )

    return {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "duration": info.get("duration"),
        "width": info.get("width"),
        "height": info.get("height"),
        "fps": info.get("fps"),
        "filepath": filepath,
    }