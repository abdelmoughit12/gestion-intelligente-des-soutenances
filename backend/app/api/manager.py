from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..db.session import get_db
from ..dependencies import require_manager
from ..models.user import User
from ..schemas.professor import ProfessorCreateData

router = APIRouter()

# ... (existing pending student routes) ...

@router.post("/professors", response_model=schemas.user.User, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_manager)])
def add_professor(
    *,
    db: Session = Depends(get_db),
    professor_in: ProfessorCreateData
):
    """
    Add a new professor to the system.
    Accessible only by managers.
    """
    # Check if a user with this email already exists
    if crud.crud_user.get_user_by_email(db, email=professor_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
    
    professor_user = crud.professor.create_with_user(db=db, obj_in=professor_in)
    return professor_user

@router.get("/pending-students", response_model=List[schemas.user.User], dependencies=[Depends(require_manager)])
def get_pending_students(db: Session = Depends(get_db)):
    """
    Get all pending student registration requests.
    Accessible only by managers.
    """
    return crud.crud_user.get_pending_students(db)

@router.patch("/pending-students/{user_id}/approve", response_model=schemas.user.User, dependencies=[Depends(require_manager)])
def approve_student_registration(user_id: int, db: Session = Depends(get_db)):
    """
    Approve a student registration request.
    Accessible only by managers.
    """
    user = crud.crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already active")
        
    return crud.crud_user.activate_user(db, user=user)

@router.delete("/pending-students/{user_id}/reject", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_manager)])
def reject_student_registration(user_id: int, db: Session = Depends(get_db)):
    """
    Reject a student registration request.
    Accessible only by managers.
    """
    user = crud.crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot reject an active user")

    crud.crud_user.delete_user(db, user=user)
    return {"message": "User registration rejected and deleted."}

