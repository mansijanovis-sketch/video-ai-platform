import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import (
    CORS_ORIGINS,
    FRAMES_DIR,
    UPLOAD_DIR,
)

from .database import Base, engine
from . import models
from .routes.videos import router as videos_router


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


@app.get("/")
def root():

    return {
        "message": "Video AI API running"
    }
