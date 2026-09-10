from __future__ import annotations

from collections import defaultdict
from typing import Any

import cv2


def aggregate_detections(
    detections: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Summarise repeated per-frame detections into useful object appearances."""

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for detection in detections:
        label = detection.get("label")
        timestamp = detection.get("timestamp")

        if label and isinstance(timestamp, (int, float)):
            groups[label].append(detection)

    summary = []

    for label, items in groups.items():
        items.sort(
            key=lambda item: item["timestamp"]
        )

        confidence = (
            sum(
                float(item.get("confidence", 0))
                for item in items
            )
            / len(items)
        )

        summary.append(
            {
                "label": label,
                "appearances": len(items),
                "first_seen": items[0]["timestamp"],
                "last_seen": items[-1]["timestamp"],
                "average_confidence": round(
                    confidence,
                    3,
                ),
            }
        )

    return sorted(
        summary,
        key=lambda item: (
            -item["appearances"],
            item["label"],
        ),
    )


def detect_scene_changes(
    frames: list[dict[str, Any]],
    threshold: float = 24.0,
) -> list[dict[str, Any]]:
    """
    Find substantial visual changes between sampled frames.

    Frames contain filepaths rather than in-memory OpenCV images.
    """

    if len(frames) < 2:
        return []

    changes = []

    previous_image = None

    for frame in frames:
        filepath = frame.get("filepath")

        if not filepath:
            continue

        current_image = cv2.imread(filepath)

        if current_image is None:
            continue

        if previous_image is not None:
            old_gray = cv2.cvtColor(
                previous_image,
                cv2.COLOR_BGR2GRAY,
            )

            new_gray = cv2.cvtColor(
                current_image,
                cv2.COLOR_BGR2GRAY,
            )

            score = float(
                cv2.absdiff(
                    old_gray,
                    new_gray,
                ).mean()
            )

            if score >= threshold:
                changes.append(
                    {
                        "timestamp": frame["timestamp"],
                        "type": "scene_change",
                        "label": "Scene change",
                        "score": round(score, 2),
                    }
                )

        previous_image = current_image

    return changes


def build_timeline(
    object_summary,
    ocr_results,
    scene_changes,
):
    """Return one chronological, frontend-friendly list of notable video events."""

    events = list(scene_changes)

    events.extend(
        {
            "timestamp": item["first_seen"],
            "type": "object",
            "label": item["label"],
            "detail": (
                f"Seen {item['appearances']} time(s)"
            ),
            "confidence": item[
                "average_confidence"
            ],
        }
        for item in object_summary
    )

    events.extend(
        {
            "timestamp": item["timestamp"],
            "type": "text",
            "label": "Visible text",
            "detail": item["text"],
        }
        for item in ocr_results
    )

    return sorted(
        events,
        key=lambda item: (
            item["timestamp"],
            item["type"],
        ),
    )