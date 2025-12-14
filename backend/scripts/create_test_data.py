"""
Script to create initial test data in the database
Run this once to set up a test student user
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.student import Student

def create_test_student():
    db = SessionLocal()
    try:
        # Check if student already exists
        existing_user = db.query(User).filter(User.email == "test.student@example.com").first()
        if existing_user:
            print("✓ Test student already exists!")
            print(f"  - User ID: {existing_user.id}")
            print(f"  - Email: {existing_user.email}")
            print(f"  - Name: {existing_user.first_name} {existing_user.last_name}")
            return

        # Create a test user
        test_user = User(
            first_name="Test",
            last_name="Student",
            email="test.student@example.com",
            hashed_password="hashed_password_placeholder",  # In production, use proper hashing
            role="student"
        )
        db.add(test_user)
        db.flush()  # Get the user ID
        
        # Create student details
        test_student = Student(
            user_id=test_user.id,
            major="Computer Science",
            cne="CNE123456789",
            year=2025
        )
        db.add(test_student)
        db.commit()
        
        print("✓ Test student created successfully!")
        print(f"  - User ID: {test_user.id}")
        print(f"  - Email: {test_user.email}")
        print(f"  - Name: {test_user.first_name} {test_user.last_name}")
        print(f"  - Major: {test_student.major}")
        print(f"  - CNE: {test_student.cne}")
        
    except Exception as e:
        print(f"✗ Error creating test student: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test data in database...")
    create_test_student()
    print("\nDatabase setup complete!")
