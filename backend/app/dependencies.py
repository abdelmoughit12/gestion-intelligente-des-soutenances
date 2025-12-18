from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.session import SessionLocal
from app.core.security import verify_token, oauth2_scheme
from app.crud import crud_user
from app.models.user import User, UserRole

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_email(db, email=user_email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_from_request_if_exists(
    request: Request, db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
            payload = verify_token(token)
            user_email: str = payload.get("sub")
            if user_email:
                user = crud_user.get_user_by_email(db, email=user_email)
                return user
    except (JWTError, HTTPException):
        pass
    return None

def require_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. User role: {current_user.role}. Required role: {required_role}"
            )
        return current_user
    return role_checker

require_student = require_role(UserRole.student)
require_professor = require_role(UserRole.professor)
require_manager = require_role(UserRole.manager)
require_admin = require_role(UserRole.admin)