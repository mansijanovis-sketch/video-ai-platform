from app.services.timeline import aggregate_detections, build_timeline


def test_aggregate_detections_groups_by_label():
    summary = aggregate_detections([
        {"label": "person", "timestamp": 0.0, "confidence": 0.9},
        {"label": "person", "timestamp": 1.0, "confidence": 0.7},
        {"label": "laptop", "timestamp": 0.0, "confidence": 0.8},
    ])
    assert summary[0]["label"] == "person"
    assert summary[0]["appearances"] == 2
    assert summary[0]["average_confidence"] == 0.8


def test_timeline_is_chronological():
    timeline = build_timeline(
        [{"label": "person", "appearances": 1, "first_seen": 2.0, "last_seen": 2.0, "average_confidence": 0.9}],
        [{"timestamp": 1.0, "text": "Welcome"}],
        [{"timestamp": 3.0, "type": "scene_change", "label": "Scene change", "score": 30}],
    )
    assert [event["timestamp"] for event in timeline] == [1.0, 2.0, 3.0]
