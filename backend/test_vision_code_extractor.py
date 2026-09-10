import pytest

from app.services.vision_code_extractor import extract_code_from_frame


def test_extract_code_from_frame_requires_api_key(
    monkeypatch,
    tmp_path,
):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    image_path = tmp_path / "test.jpg"
    image_path.write_bytes(b"fake-image")

    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY is not configured",
    ):
        extract_code_from_frame(
            filepath=str(image_path),
            timestamp=10.0,
            filename_hint="App.js",
        )