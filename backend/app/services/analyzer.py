import os

from .video_processor import extract_frames
from .detector import detect_objects
from .ocr import extract_text
from .ocr_cleaner import clean_ocr_text
from .vision import generate_video_description
from .timeline import aggregate_detections, build_timeline, detect_scene_changes

from ..models import Detection


def analyze_video(
    video_path: str,
    video_id: int,
    db,
    video_duration: float,
):

    output_dir = os.path.join(
        "frames",
        str(video_id),
    )

    frames = extract_frames(
        video_path,
        output_dir,
        interval_seconds=1.0,
    )

    detection_count = 0

    all_detections = []

    ocr_results = []

    # --------------------------------------------------
    # Analyze every frame
    # --------------------------------------------------

    for frame in frames:

        # ==================================================
        # YOLO OBJECT DETECTION
        # ==================================================

        detections = detect_objects(
            frame["filepath"]
        )

        for detection in detections:

            all_detections.append(
                {
                    **detection,
                    "timestamp": frame["timestamp"],
                }
            )

            db_detection = Detection(
                video_id=video_id,
                timestamp=frame["timestamp"],
                label=detection["label"],
                confidence=detection["confidence"],
                x1=detection["x1"],
                y1=detection["y1"],
                x2=detection["x2"],
                y2=detection["y2"],
            )

            db.add(
                db_detection
            )

            detection_count += 1

        # ==================================================
        # OCR TEXT DETECTION
        # ==================================================

        raw_text = extract_text(
            frame["filepath"]
        )

        text = clean_ocr_text(
            raw_text
        )

        if text:

            ocr_results.append(
                {
                    "timestamp": frame["timestamp"],
                    "text": text,
                }
            )

    object_summary = aggregate_detections(all_detections)
    scene_changes = detect_scene_changes(frames)
    timeline = build_timeline(object_summary, ocr_results, scene_changes)

    db.commit()

    # --------------------------------------------------
    # Generate local video description
    # --------------------------------------------------

    description = generate_video_description(
        frames=frames,
        detections=all_detections,
        video_duration=video_duration,
        ocr_results=ocr_results,
    )

    return {
        "frames_processed": len(frames),
        "detections_created": detection_count,
        "description": description,
        "ocr_results": ocr_results,
        "object_summary": object_summary,
        "scene_changes": scene_changes,
        "timeline": timeline,
    }
