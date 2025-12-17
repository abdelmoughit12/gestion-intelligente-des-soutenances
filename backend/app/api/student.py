from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from pathlib import Path
import os
import shutil
from uuid import uuid4

from .. import schemas, models
from .. import crud
from ..db.session import get_db, SessionLocal
from ..models import ThesisDefense, Report, Student

# Use the same router and db dependency pattern as professor.py
router = APIRouter(prefix="/api/students", tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the storage path consistent with the professor API
UPLOAD_DIR = Path("storage/reports")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10MB
ALLOWED_PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/acrobat", "applications/vnd.pdf"}

def _sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    name = name.replace(" ", "_")
    keep = []
    for ch in name:
        if ch.isalnum() or ch in {"_", "-", "."}:
            keep.append(ch)
    sanitized = "".join(keep)
    return sanitized or "upload.pdf"

@router.post("/soutenance-requests", response_model=schemas.ThesisDefense)
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
    if not pdf.filename or not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if pdf.content_type and pdf.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid PDF content type")

    # Use the file saving logic from HEAD, which is simpler and consistent.
    file_extension = os.path.splitext(pdf.filename)[1]
    new_filename = f"report_student_{student_id}_{title.replace(' ', '_')}_{uuid4().hex[:6]}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, new_filename)

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(pdf.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create Report and ThesisDefense records as in HEAD
    new_report = Report(
        file_name=new_filename,
        file_path=str(file_location),
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    new_thesis_defense = ThesisDefense(
        title=title,
        student_id=student_id,
        report_id=new_report.id,
        status="pending"
    )
    db.add(new_thesis_defense)

    # Manually update student's domain if provided
    student = db.query(Student).filter(Student.user_id == student_id).first()
    if student:
        student.major = domain
    
    db.commit()
    db.refresh(new_thesis_defense)

    return new_thesis_defense


@router.get("/soutenance-requests", response_model=List[schemas.ThesisDefense])
def get_student_requests(
    db: Session = Depends(get_db),
    student_id: int = 1,  # TODO: Get from authenticated user session
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all soutenance requests for a specific student.
    """
    defenses = db.query(ThesisDefense).filter(ThesisDefense.student_id == student_id).offset(skip).limit(limit).all()
    return defenses


@router.get("/dashboard", response_model=schemas.StudentDashboardStats)
def get_student_dashboard(
    db: Session = Depends(get_db),
    student_id: int = 1,  # TODO: Get from authenticated user session
):
    """
    Get dashboard statistics for a student.
    """
    defenses = db.query(ThesisDefense).filter(ThesisDefense.student_id == student_id).all()

    today = date.today()
    upcoming_cutoff = today + timedelta(days=7)
    upcoming = [
        d
        for d in defenses
        if d.defense_date is not None and today <= d.defense_date <= upcoming_cutoff
    ]

    return schemas.StudentDashboardStats(
        total=len(defenses),
        pending=sum(1 for d in defenses if d.status == "pending"),
        accepted=sum(1 for d in defenses if d.status == "accepted"),
        refused=sum(1 for d in defenses if d.status == "refused"),
        recent_requests=defenses[:5],
        upcoming_defenses=upcoming,
    )


@router.get("/requests/{defense_id}", response_model=schemas.ThesisDefense)
def get_single_request(
    *,
    db: Session = Depends(get_db),
    defense_id: int,
    student_id: int = 1,  # TODO: Get from authenticated user session
):
    """
    Get details of a specific soutenance request.
    """
    defense = db.query(ThesisDefense).filter(ThesisDefense.id == defense_id).first()
    if not defense:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if defense.student_id != student_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    
    return defense
