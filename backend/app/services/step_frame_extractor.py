import os

import cv2


def extract_step_frames(
    video_path: str,
    output_dir: str,
    steps: list[dict],
    padding_seconds: float = 2.0,
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

    extracted_frames = []

    for step in steps:

        start_time = max(
            step["start_time"]
            - padding_seconds,
            0,
        )

        end_time = (
            step["end_time"]
            + padding_seconds
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
                    f"step_{step['step']}_"
                    f"{timestamp:.2f}.jpg"
                )

                filepath = os.path.join(
                    output_dir,
                    filename,
                )

                cv2.imwrite(
                    filepath,
                    frame,
                )

                extracted_frames.append(
                    {
                        "step": step["step"],
                        "filepath": filepath,
                        "timestamp": timestamp,
                    }
                )

            frame_index += 1

    cap.release()

    return extracted_frames