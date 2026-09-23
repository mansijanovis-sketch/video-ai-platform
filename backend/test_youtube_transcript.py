import requests
import pytest

from app.services import youtube_transcript as service


VIDEO_ID = "S66rHpyU-Eg"


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self.payload = payload

    def json(self):
        return self.payload


def test_supadata_transcript_normalizes_timestamped_segments(monkeypatch):
    monkeypatch.setattr(service, "SUPADATA_API_KEY", "test-key")
    monkeypatch.setattr(
        service.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(
            200,
            {
                "content": [
                    {"text": " first step ", "offset": 1250, "duration": 800},
                    {"text": "", "offset": 2100, "duration": 100},
                ],
                "lang": "en",
            },
        ),
    )

    result = service.fetch_youtube_transcript(VIDEO_ID)

    assert result["video_id"] == VIDEO_ID
    assert result["language"] == "en"
    assert result["language_code"] == "en"
    assert result["is_generated"] is False
    assert result["segments"] == [
        {
            "start_time": 1.25,
            "end_time": 2.05,
            "text": "first step",
        }
    ]


def test_local_provider_preserves_generated_transcript(monkeypatch):
    class Snippet:
        start = 3
        duration = 1.5
        text = "Generated caption"

    class Transcript:
        language = "English"
        language_code = "en"
        is_generated = True

        def __iter__(self):
            return iter([Snippet()])

    class Api:
        def fetch(self, video_id, languages):
            assert video_id == VIDEO_ID
            assert languages == ["en"]
            return Transcript()

    monkeypatch.setattr(service, "SUPADATA_API_KEY", None)
    monkeypatch.setattr(service, "YouTubeTranscriptApi", Api)

    result = service.fetch_youtube_transcript(VIDEO_ID)

    assert result["language"] == "English"
    assert result["language_code"] == "en"
    assert result["is_generated"] is True
    assert result["segments"][0]["end_time"] == 4.5


def test_provider_reports_transcript_unavailable(monkeypatch):
    monkeypatch.setattr(service, "SUPADATA_API_KEY", "test-key")
    monkeypatch.setattr(
        service.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(
            206,
            {"error": "transcript-unavailable"},
        ),
    )

    with pytest.raises(service.TranscriptUnavailableError):
        service.fetch_youtube_transcript(VIDEO_ID)


def test_provider_reports_access_blocked(monkeypatch):
    monkeypatch.setattr(service, "SUPADATA_API_KEY", "test-key")
    monkeypatch.setattr(
        service.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(
            403,
            {"error": "forbidden"},
        ),
    )

    with pytest.raises(service.TranscriptAccessBlockedError):
        service.fetch_youtube_transcript(VIDEO_ID)


def test_provider_failure_is_typed(monkeypatch):
    monkeypatch.setattr(service, "SUPADATA_API_KEY", "test-key")

    def fail_request(*args, **kwargs):
        raise requests.Timeout("provider timeout")

    monkeypatch.setattr(service.requests, "get", fail_request)

    with pytest.raises(service.TranscriptProviderError):
        service.fetch_youtube_transcript(VIDEO_ID)