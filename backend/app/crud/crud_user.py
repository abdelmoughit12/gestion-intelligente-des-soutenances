from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..core.security import get_password_hash, verify_password
from ..schemas.user import UserCreate

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        cni=user.cni
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def check_user_exists(db: Session, email: str) -> bool:
    """Check if a user with the given email exists."""
    return get_user_by_email(db, email=email) is not None