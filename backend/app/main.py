from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import Base, engine, and SessionLocal from the database session module
from .db.session import Base, engine, SessionLocal
from . import models

# Import les routers d'API
from .api import professor, student

# This line will create the database tables if they don't exist
# as soon as the application starts.
# When we define our models, they will inherit from Base, and so
# they will be registered with this metadata.
# Note: For production, you would typically use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Application with PostgreSQL")

# ===== CORS MIDDLEWARE =====
# Permet au frontend (localhost:3000) d'appeler le backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ENREGISTRER LES ROUTERS =====
# Un router regroupe plusieurs endpoints
# Include = ajouter tous les endpoints du router à l'app

app.include_router(professor.router)
app.include_router(student.router)

# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}