from app.services.vision import generate_video_description


def test_generate_video_description_with_objects():
    frames = [
        {
            "filepath": "frame_0.00.jpg",
            "timestamp": 0.0,
        },
        {
            "filepath": "frame_1.00.jpg",
            "timestamp": 1.0,
        },
    ]

    detections = [
        {
            "label": "laptop",
            "confidence": 0.95,
            "x1": 10,
            "y1": 20,
            "x2": 300,
            "y2": 200,
            "timestamp": 0.0,
        },
        {
            "label": "person",
            "confidence": 0.90,
            "x1": 50,
            "y1": 30,
            "x2": 250,
            "y2": 300,
            "timestamp": 1.0,
        },
    ]

    result = generate_video_description(
        frames=frames,
        detections=detections,
        video_duration=2.0,
        ocr_results=[],
    )

    assert "2.0 seconds" in result
    assert "laptop" in result
    assert "person" in result
    assert "computer or electronic device" in result


def test_generate_video_description_with_ocr():
    frames = [
        {
            "filepath": "frame_0.00.jpg",
            "timestamp": 0.0,
        }
    ]

    detections = []

    ocr_results = [
        {
            "timestamp": 0.0,
            "text": "React CRUD Application",
        }
    ]

    result = generate_video_description(
        frames=frames,
        detections=detections,
        video_duration=1.0,
        ocr_results=ocr_results,
    )

    assert "1.0 seconds" in result
    assert "React CRUD Application" in result


def test_generate_video_description_without_frames():
    result = generate_video_description(
        frames=[],
        detections=[],
        video_duration=0,
        ocr_results=[],
    )

    assert result == "No frames were available for analysis."