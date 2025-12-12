from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from .. import crud
from ..db.session import get_db

router = APIRouter()

@router.get("/professors/", response_model=List[schemas.Professor])
def read_professors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all professors.
    """
    professors = crud.professor.get_multi(db, skip=skip, limit=limit)
    return professors

@router.get("/professors/{professor_id}", response_model=schemas.Professor)
def read_professor(
    *,
    db: Session = Depends(get_db),
    professor_id: int
):
    """
    Get a specific professor by ID.
    """
    professor = crud.professor.get(db=db, id=professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor
