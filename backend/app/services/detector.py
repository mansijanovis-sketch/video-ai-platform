from ultralytics import YOLO


model = YOLO("yolo11n.pt")


def detect_objects(image_path: str):

    results = model(
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

            label = model.names[
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