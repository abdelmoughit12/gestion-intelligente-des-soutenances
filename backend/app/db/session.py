import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the SQLAlchemy engine
# For PostgreSQL, we don't need connect_args={"check_same_thread": False}
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
# Each instance of the SessionLocal class will be a database session.
# The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This will be the base class for our models.
Base = declarative_base()
