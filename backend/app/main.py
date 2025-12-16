from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .db.session import Base, engine
from . import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soutenance Manager API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Routers
from .api import thesis_defense, professor, stats, student

app.include_router(thesis_defense.router, prefix="/api/v1", tags=["thesis-defenses"])
app.include_router(professor.router, prefix="/api/v1", tags=["professors"])
app.include_router(student.router, prefix="/api", tags=["students"])
app.include_router(stats.router, prefix="/api", tags=["statistics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
