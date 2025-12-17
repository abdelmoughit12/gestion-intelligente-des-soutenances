from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..schemas.user import User as UserSchema
from ..models.user import User as UserModel

router = APIRouter()

@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current authenticated user",
    description="""
    Retrieves the profile information of the currently authenticated user.
    Requires a valid JWT access token in the `Authorization` header.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Successful retrieval of user profile",
            "content": {
                "application/json": {
                    "example": {
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "cni": "123456789",
                        "role": "student",
                        "id": 1
                    }
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication required or invalid token",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            },
        },
    },
)
def read_current_user(
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get current authenticated user.
    """
    return current_user
