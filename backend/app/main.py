import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from . import models
from .routes.videos import router as videos_router


# Make sure required directories exist
os.makedirs(
    "uploads",
    exist_ok=True,
)

os.makedirs(
    "frames",
    exist_ok=True,
)


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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve uploaded videos
app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads"
    ),
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
