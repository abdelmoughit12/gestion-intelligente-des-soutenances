from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import schemas, models
from .. import crud
from ..db.session import get_db
from ..services import jury_ai
from ..dependencies import get_current_user, require_manager

router = APIRouter()

# Response model for jury suggestions
class JurySuggestion(BaseModel):
    professor_id: int
    name: str
    reason: str

@router.get("/", response_model=List[schemas.ThesisDefense])
def read_thesis_defenses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Retrieve all thesis defenses.
    """
    defenses = crud.thesis_defense.get_multi(db, skip=skip, limit=limit)
    return defenses


@router.patch("/{defense_id}", response_model=schemas.ThesisDefense)
def update_thesis_defense(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    defense_in: schemas.ThesisDefenseUpdate,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Update a thesis defense (e.g., to accept/refuse or schedule it).
    """
    defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not defense:
        raise HTTPException(status_code=404, detail="Thesis defense not found")
    updated_defense = crud.thesis_defense.update(db=db, db_obj=defense, obj_in=defense_in)
    return updated_defense


@router.get("/{defense_id}/jury", response_model=List[schemas.JuryMember])
def read_jury_for_defense(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Retrieve jury members for a specific thesis defense.
    """
    jury_members = crud.jury_member.get_by_defense(db=db, defense_id=defense_id)
    return jury_members


@router.post("/{defense_id}/jury", response_model=schemas.JuryMember)
def create_jury_member_for_defense(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    jury_member_in: schemas.JuryMemberCreate,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Assign a professor to the jury for a specific thesis defense.
    """
    # Check if thesis defense exists
    thesis_defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not thesis_defense:
        raise HTTPException(status_code=404, detail="Thesis defense not found")

    # Check if professor exists
    professor = crud.professor.get(db=db, id=jury_member_in.professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    # Ensure the defense_id in path matches the one in the request body
    if jury_member_in.thesis_defense_id != defense_id:
        raise HTTPException(status_code=400, detail="Thesis defense ID in path and body must match.")

    # Check if this professor is already in the jury for this defense
    existing_jury_member = db.query(models.JuryMember).filter(
        models.JuryMember.thesis_defense_id == defense_id,
        models.JuryMember.professor_id == jury_member_in.professor_id
    ).first()
    if existing_jury_member:
        raise HTTPException(status_code=409, detail="Professor already assigned to this jury.")

    jury_member = crud.jury_member.create(db=db, obj_in=jury_member_in)
    return jury_member


@router.put("/{defense_id}/jury/{professor_id}", response_model=schemas.JuryMember)
def update_jury_member(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    professor_id: int,
    jury_member_in: schemas.JuryMemberUpdate,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Update a jury member for a specific thesis defense.
    """
    # Check if thesis defense exists
    thesis_defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not thesis_defense:
        raise HTTPException(status_code=404, detail="Thesis defense not found")

    # Get the specific jury member using defense_id and professor_id
    jury_member = crud.jury_member.get(db=db, thesis_defense_id=defense_id, professor_id=professor_id)
    if not jury_member:
        raise HTTPException(status_code=404, detail="Jury member not found for this defense and professor")

    # Ensure the jury member belongs to the correct defense (redundant if using composite key, but good for safety)
    if jury_member.thesis_defense_id != defense_id or jury_member.professor_id != professor_id:
        raise HTTPException(status_code=400, detail="Jury member does not match the provided defense or professor IDs")

    updated_jury_member = crud.jury_member.update(db=db, db_obj=jury_member, obj_in=jury_member_in)
    return updated_jury_member


@router.get("/{defense_id}/jury-suggestions", response_model=List[JurySuggestion])
def get_jury_suggestions(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    num_suggestions: int = 3,
    current_user: models.user.User = Depends(require_manager)
):
    """
    Get AI-powered jury member suggestions for a thesis defense based on domain expertise.
    """
    # Get the thesis defense
    defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not defense:
        raise HTTPException(status_code=404, detail="Thesis defense not found")
    
    # Get available professors
    professors = crud.professor.get_multi(db=db)
    available_profs = [
        {
            "id": p.user_id,
            "name": f"{p.user.first_name} {p.user.last_name}" if p.user else f"Professor {p.user_id}",
            "specialty": p.specialty or "General"
        }
        for p in professors
    ]
    
    # Get thesis domain from report
    thesis_domain = "General"
    thesis_title = defense.title or "Untitled Thesis"
    
    if defense.report and defense.report.ai_domain:
        try:
            import json
            thesis_domain = json.loads(defense.report.ai_domain)
        except:
            thesis_domain = defense.report.ai_domain
    
    # Get AI suggestions
    suggestions = jury_ai.suggest_jury_members(
        thesis_title=thesis_title,
        thesis_domain=thesis_domain,
        available_professors=available_profs,
        num_suggestions=num_suggestions
    )
    
    return suggestions
