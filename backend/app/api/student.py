from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path
import os

from .. import schemas, models
from .. import crud
from ..db.session import get_db

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/students/soutenance-requests", response_model=schemas.ThesisDefense)
async def create_soutenance_request(
    *,
    db: Session = Depends(get_db),
    title: str = Form(...),
    domain: str = Form(...),
    pdf: UploadFile = File(...),
    student_id: int = Form(1),  # TODO: Get from authenticated user session
):
    """
    Create a new soutenance request (thesis defense).
    Uploads PDF report, creates report entry, and creates thesis defense entry.
    """
    # Validate PDF file
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save PDF file to disk
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{timestamp}_{pdf.filename}"
    file_path = os.path.join("uploads", safe_filename)
    
    try:
        # Write file to disk
        with open(file_path, "wb") as buffer:
            content = await pdf.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # TODO: Implement AI analysis for summary, domain detection, and similarity score
    # This would call your AI service here
    ai_summary = f"AI-generated summary for {title}. This will be implemented with actual AI integration."
    ai_domain = domain  # For now, use the domain provided by student
    ai_similarity_score = None  # Will be calculated by AI
    
    # Create Report entry with the saved file path
    report_data = schemas.ReportCreate(
        file_name=file_path,  # Store the full path to the saved file
        ai_summary=ai_summary,
        ai_domain=ai_domain,
        ai_similarity_score=ai_similarity_score,
        student_id=student_id
    )
    report = crud.report.create(db=db, obj_in=report_data)
    
    # Create ThesisDefense entry
    defense_data = schemas.ThesisDefenseCreate(
        title=title,
        description=f"Thesis defense for {title} in {domain} domain",
        status="pending",
        student_id=student_id,
        report_id=report.id
    )
    defense = crud.thesis_defense.create(db=db, obj_in=defense_data)
    
    return defense


@router.get("/students/soutenance-requests", response_model=List[schemas.ThesisDefense])
def get_student_requests(
    db: Session = Depends(get_db),
    student_id: int = 1,  # TODO: Get from authenticated user session
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all soutenance requests for a specific student.
    """
    defenses = crud.thesis_defense.get_by_student(db=db, student_id=student_id, skip=skip, limit=limit)
    return defenses


@router.get("/students/dashboard")
def get_student_dashboard(
    db: Session = Depends(get_db),
    student_id: int = 1,  # TODO: Get from authenticated user session
):
    """
    Get dashboard statistics for a student.
    Returns count of pending, accepted, and refused requests.
    """
    defenses = crud.thesis_defense.get_by_student(db=db, student_id=student_id)
    
    stats = {
        "total": len(defenses),
        "pending": sum(1 for d in defenses if d.status == "pending"),
        "accepted": sum(1 for d in defenses if d.status == "accepted"),
        "refused": sum(1 for d in defenses if d.status == "refused"),
    }
    
    return stats


@router.get("/students/requests/{defense_id}", response_model=schemas.ThesisDefense)
def get_single_request(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    student_id: int = 1,  # TODO: Get from authenticated user session
):
    """
    Get details of a specific soutenance request.
    """
    defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not defense:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Ensure the request belongs to this student
    if defense.student_id != student_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    
    return defense
