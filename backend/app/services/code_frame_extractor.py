import os

import cv2


def extract_code_frames(
    video_path: str,
    output_dir: str,
    start_time: float,
    end_time: float,
    interval_seconds: float = 2.0,
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

    start_frame = int(
        start_time * fps
    )

    end_frame = int(
        end_time * fps
    )

    frame_interval = max(
        int(interval_seconds * fps),
        1,
    )

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        start_frame,
    )

    frame_index = start_frame

    saved_frames = []

    while frame_index <= end_frame:

        success, frame = cap.read()

        if not success:
            break

        if (
            frame_index - start_frame
        ) % frame_interval == 0:

            timestamp = (
                frame_index / fps
            )

            filename = (
                f"code_{timestamp:.2f}.jpg"
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
                }
            )

        frame_index += 1

    cap.release()

    return saved_frames