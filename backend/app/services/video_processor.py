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

    if fps <= 0:
        cap.release()
        raise ValueError(
            "Could not determine video FPS"
        )

    frame_interval = max(
        int(fps * interval_seconds),
        1,
    )

    frame_index = 0

    saved_frames = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_index % frame_interval == 0:

            timestamp = (
                frame_index / fps
            )

            filename = (
                f"frame_{timestamp:.2f}.jpg"
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
        "timestamp": timestamp,
        "frame": frame.copy(),
    }
)

        frame_index += 1

    cap.release()

    return saved_frames