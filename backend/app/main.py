from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Import Base, engine, and SessionLocal from the database session module
from .db.session import Base, engine, SessionLocal
from . import models

# This line will create the database tables if they don't exist
# as soon as the application starts.
# When we define our models, they will inherit from Base, and so
# they will be registered with this metadata.
# Note: For production, you would typically use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Application with PostgreSQL")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from .api import thesis_defense
from .api import professor # New import
from .api import stats # New import for stats

app.include_router(thesis_defense.router, prefix="/api", tags=["thesis-defenses"])
app.include_router(professor.router, prefix="/api", tags=["professors"]) # New router inclusion
app.include_router(stats.router, prefix="/api", tags=["statistics"]) # New router inclusion for stats


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}