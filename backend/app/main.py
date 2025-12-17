from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import Base, engine, and SessionLocal from the database session module
from app.db.session import Base, engine, SessionLocal
from app import models

# This line will create the database tables if they don't exist
# as soon as the application starts.
# When we define our models, they will inherit from Base, and so
# they will be registered with this metadata.
# Note: For production, you would typically use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soutenance Manager API")

from app.middleware import ExceptionHandlerMiddleware, LoggingMiddleware, SecurityHeadersMiddleware

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Configure CORS for frontend
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(',')],  # Frontend URLs loaded from settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Serve uploaded files
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

from app.api import thesis_defense, professor, student, auth, user

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(thesis_defense.router, prefix="/api/v1/thesis-defenses", tags=["thesis-defenses"])
app.include_router(professor.router, prefix="/api/v1/professors", tags=["professors"])
app.include_router(student.router, prefix="/api/v1/students", tags=["students"])

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Soutenance Manager API",
        version="1.0.0",
        description="API for managing thesis defenses, including student submissions, professor evaluations, and administrative oversight. This API provides secure access via JWT authentication for different user roles (student, professor, manager, admin).",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format 'Bearer <token>'"
        }
    }
    # Apply security to all endpoints globally.
    # Individual endpoints can override this with their own security parameter.
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}