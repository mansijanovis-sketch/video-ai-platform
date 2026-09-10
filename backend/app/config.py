import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured."
    )


TESSERACT_PATH = os.getenv(
    "TESSERACT_PATH",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
)


UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    "uploads",
)


FRAMES_DIR = os.getenv(
    "FRAMES_DIR",
    "frames",
)


SMART_SAMPLING_ENABLED = os.getenv(
    "SMART_SAMPLING_ENABLED",
    "true",
).strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}


SMART_SAMPLING_COARSE_INTERVAL = float(
    os.getenv(
        "SMART_SAMPLING_COARSE_INTERVAL",
        "5.0",
    )
)


SMART_SAMPLING_VISUAL_THRESHOLD = float(
    os.getenv(
        "SMART_SAMPLING_VISUAL_THRESHOLD",
        "18.0",
    )
)


SMART_SAMPLING_REFINEMENT_WINDOW = float(
    os.getenv(
        "SMART_SAMPLING_REFINEMENT_WINDOW",
        "3.0",
    )
)


SMART_SAMPLING_REFINEMENT_INTERVAL = float(
    os.getenv(
        "SMART_SAMPLING_REFINEMENT_INTERVAL",
        "1.0",
    )
)


SMART_SAMPLING_MIN_FRAME_GAP = float(
    os.getenv(
        "SMART_SAMPLING_MIN_FRAME_GAP",
        "1.0",
    )
)


CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]