from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .db.session import Base, engine
from . import models

# Import all API routers
from .api import professor, student, thesis_defense, stats

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soutenance Manager API")

# ===== CORS MIDDLEWARE =====
# Combine origins from both branches for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001", # from dev branch
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== STATIC FILE SERVING =====
# Serve reports from the storage/reports directory, consistent with other modules
REPORTS_DIR = Path(__file__).resolve().parent / "storage" / "reports"
REPORTS_DIR.mkdir(exist_ok=True, parents=True)
app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR)), name="reports")


# ===== REGISTER ROUTERS =====
# Include all routers. Prefixes are defined within each router file.
app.include_router(professor.router)
app.include_router(student.router)
app.include_router(thesis_defense.router)
app.include_router(stats.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Soutenance Manager API!"}
