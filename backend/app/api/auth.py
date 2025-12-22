from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..schemas import token
from ..schemas.user import StudentRegistration
from ..crud import crud_user, crud_student
from ..core import security
from ..db.session import get_db
from ..core.config import settings
from ..models.user import User

router = APIRouter()


@router.post("/register/student", status_code=status.HTTP_201_CREATED)
def register_student(
    *,
    db: Session = Depends(get_db),
    student_in: StudentRegistration
):
    """
    Create a new student registration request.
    The account will be inactive until approved by a manager.
    """
    # Check for existing user with the same email
    if crud_user.get_user_by_email(db, email=student_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
    # Check for existing user with the same CNI
    if crud_student.get_user_by_cni(db, cni=student_in.cni):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this CNI already exists.",
        )
    # Check for existing student with the same CNE
    if crud_student.get_student_by_cne(db, cne=student_in.cne):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this CNE already exists.",
        )

    user = crud_student.create_student_registration(db, student_in=student_in)
    
    return {"message": "Registration successful. Your account is pending approval."}


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
