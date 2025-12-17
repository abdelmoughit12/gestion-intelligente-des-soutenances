import asyncio
import sys
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.db.session import SessionLocal
from app.crud import crud_user
from app.schemas.user import UserCreate
from app.models.user import UserRole

async def create_initial_users():
    db: Session = SessionLocal()
    users_to_create = [
        {
            "email": "student@example.com",
            "password": "password",
            "first_name": "Student",
            "last_name": "User",
            "role": UserRole.student,
            "cni": "ST12345"
        },
        {
            "email": "professor@example.com",
            "password": "password",
            "first_name": "Professor",
            "last_name": "User",
            "role": UserRole.professor,
            "cni": "PR12345"
        },
        {
            "email": "manager@example.com",
            "password": "password",
            "first_name": "Manager",
            "last_name": "User",
            "role": UserRole.manager,
            "cni": "MA12345"
        },
        {
            "email": "admin@example.com",
            "password": "password",
            "first_name": "Admin",
            "last_name": "User",
            "role": UserRole.admin,
            "cni": "AD12345"
        },
    ]

    for user_data in users_to_create:
        user = crud_user.get_user_by_email(db, email=user_data["email"])
        if not user:
            user_in = UserCreate(**user_data)
            crud_user.create_user(db, user=user_in)
            print(f"User {user_data['email']} created")
        else:
            print(f"User {user_data['email']} already exists")

    db.close()

if __name__ == "__main__":
    print("Creating initial data...")
    asyncio.run(create_initial_users())
    print("Initial data created.")
