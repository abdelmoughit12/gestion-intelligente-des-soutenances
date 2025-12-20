from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..schemas import token
from ..crud import crud_user
from ..core import security
from ..db.session import get_db
from ..core.config import settings
from ..models.user import User

router = APIRouter()

@router.post(
    "/login",
    response_model=token.Token,
    summary="Authenticate user and receive JWT token",
    description="""
    Authenticates a user with provided email and password.
    Upon successful authentication, a JWT access token is returned.
    This token must be included in the `Authorization` header of subsequent requests
    to access protected endpoints (e.g., `Bearer YOUR_ACCESS_TOKEN`).
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Authentication",
            "content": {
                "application/json": {
                    "example": {"access_token": "your_jwt_token_here", "token_type": "bearer"}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        },
    },
)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # First check if user exists
    user_exists = crud_user.check_user_exists(db, email=form_data.username)
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found. Please register first.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Try to authenticate
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    if not user:
        # User exists but password is wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role.value, "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
