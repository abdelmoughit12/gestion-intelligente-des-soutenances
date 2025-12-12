from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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

# We will add more endpoints that interact with the database in the next steps.