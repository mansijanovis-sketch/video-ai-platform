from pathlib import Path

from ultralytics import YOLO

from ..config import YOLO_MODEL_PATH


model = None


def _get_model():
    global model

    if model is None:
        model_path = Path(YOLO_MODEL_PATH)
        if not model_path.is_file():
            raise RuntimeError(
                "YOLO model file is not available for video analysis."
            )
        model = YOLO(str(model_path))

    return model


def detect_objects(image_path: str):
    detector = _get_model()

    results = detector(
        image_path
    )

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            x1, y1, x2, y2 = map(
                float,
                box.xyxy[0],
            )

            label = detector.names[
                class_id
            ]

            detections.append(
                {
                    "label": label,
                    "confidence": confidence,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                }
            )

    return detections