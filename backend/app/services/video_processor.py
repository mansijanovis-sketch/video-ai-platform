import os

import cv2


def get_video_info(video_path: str):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(
            "Could not open video"
        )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    frame_count = cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )

    duration = (
        frame_count / fps
        if fps > 0
        else 0
    )

    cap.release()

    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration,
    }


def extract_frames(
    video_path: str,
    output_dir: str,
    interval_seconds: float = 1.0,
):
    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    cap = cv2.VideoCapture(
        video_path
    )

    if not cap.isOpened():
        raise ValueError(
            "Could not open video"
        )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    frame_count = cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )

    if fps <= 0:
        cap.release()

        raise ValueError(
            "Could not determine video FPS"
        )

    duration = (
        frame_count / fps
        if frame_count > 0
        else 0
    )

    interval_seconds = max(
        float(interval_seconds),
        0.1,
    )

    saved_frames = []

    timestamp = 0.0

    while timestamp < duration:

        cap.set(
            cv2.CAP_PROP_POS_MSEC,
            timestamp * 1000.0,
        )

        success, frame = cap.read()

        if not success:
            timestamp += interval_seconds
            continue

        actual_frame_index = cap.get(
            cv2.CAP_PROP_POS_FRAMES
        ) - 1

        actual_timestamp = (
            actual_frame_index / fps
        )

        filename = (
            f"frame_{actual_timestamp:.2f}.jpg"
        )

        filepath = os.path.join(
            output_dir,
            filename,
        )

        cv2.imwrite(
            filepath,
            frame,
        )

        saved_frames.append(
            {
                "filepath": filepath,
                "timestamp": actual_timestamp,
            }
        )

        timestamp += interval_seconds

    cap.release()

    return saved_frames