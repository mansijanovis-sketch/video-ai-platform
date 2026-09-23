import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from .config import (
    CORS_ORIGINS,
    FRAMES_DIR,
    UPLOAD_DIR,
)

from .database import Base, SessionLocal, engine
from . import models
from .routes.ask import router as ask_router
from .routes.early_access import router as early_access_router
from .routes.videos import router as videos_router
from .routes.transcript import router as transcript_router
from .routes.youtube import router as youtube_router


# Make sure required directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)


# Create database tables
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Video AI Platform",
    version="1.0.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve uploaded videos
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads",
)


# API routes
app.include_router(
    videos_router
)
app.include_router(transcript_router)
app.include_router(
    ask_router
)
app.include_router(
    youtube_router
)
app.include_router(
    early_access_router
)


@app.get("/")
def root():

    return {
        "message": "Video AI API running"
    }


@app.get("/health")
def health_check():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        return {
            "status": "degraded",
            "database": "unavailable",
        }

    return {
        "status": "ok",
        "database": "ok",
    }
