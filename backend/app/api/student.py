from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import date, timedelta
from pathlib import Path
import os
import shutil
from uuid import uuid4
import logging
import json

from .. import schemas, models, crud
from ..services import ai
from ..db.session import get_db
from ..dependencies import require_student
from ..models import ThesisDefense, Report, Student

router = APIRouter()

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
    current_user: models.user.User = Depends(require_student)
):
    """
    Create a new soutenance request (thesis defense).
    Uploads PDF report, creates report entry, and creates thesis defense entry.
    """
    student_id = current_user.id
    # Validate PDF file
    if not pdf.filename or not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if pdf.content_type and pdf.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid PDF content type")

    file_extension = os.path.splitext(pdf.filename)[1]
    new_filename = f"report_student_{student_id}_{title.replace(' ', '_')}_{uuid4().hex[:6]}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, new_filename)

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(pdf.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        try:
            await pdf.close()
        except Exception:
            pass

    # AI (Gemini) with safe fallbacks - pass actual PDF path for text extraction
    logger = logging.getLogger(__name__)
    
    abs_path = Path(file_location).resolve()
    rel_path = new_filename
    
    logger.info(f"\n{'='*70}")
    logger.info(f"AI PROCESSING START - Title: {title}")
    logger.info(f"PDF Path: {abs_path}")
    logger.info(f"Student Claimed Domain: {domain}")
    logger.info(f"{'='*70}")
    
    # Extract and log PDF content
    pdf_text = ai.extract_pdf_text(str(abs_path))
    logger.info(f"Extracted PDF Text: {len(pdf_text)} characters")
    logger.info(f"Preview: {pdf_text[:200]}...")
    
    # Generate summary
    logger.info("\nGenerating AI Summary...")
    ai_summary = ai.summarize(title, pdf_path=str(abs_path))
    logger.info(f"AI Summary: {ai_summary}")
    
    # Get domain confidence scores
    logger.info("\nClassifying Domain...")
    domain_confidence = ai.classify_domain(title, domain, pdf_path=str(abs_path))
    logger.info(f"Domain Confidence: {domain_confidence}")
    # Store as JSON string for database
    ai_domain = json.dumps(domain_confidence)
    
    # Calculate similarity with previous reports
    logger.info("\nCalculating Similarity...")
    prior_defenses = crud.thesis_defense.get_by_student(db=db, student_id=student_id)
    prior_reports = []
    for defense in prior_defenses:
        if defense.report:
            prior_reports.append({
                'id': defense.id,
                'title': defense.title,
                'content': defense.report.ai_summary or defense.title
            })
    
    similarity_result = ai.similarity_score(title, prior_reports, pdf_path=str(abs_path))
    logger.info(f"Similarity Result: {similarity_result}")
    # Store similarity as float (max similarity score)
    ai_similarity_score = similarity_result['max_similarity'] if similarity_result else 0.0
    
    logger.info(f"\n{'='*70}")
    logger.info("AI PROCESSING COMPLETE")
    logger.info(f"{'='*70}\n")
    
    # Create Report entry with the saved relative path
    report_data = schemas.ReportCreate(
        file_name=rel_path,
        ai_summary=ai_summary,
        ai_domain=ai_domain,
        ai_similarity_score=ai_similarity_score,
        student_id=student_id
    )
    new_report = crud.report.create(db=db, obj_in=report_data)
    
    # Create ThesisDefense entry
    defense_data = schemas.ThesisDefenseCreate(
        title=title,
        student_id=student_id,
        report_id=new_report.id,
        status="pending"
    )
    new_thesis_defense = crud.thesis_defense.create(db=db, obj_in=defense_data)
    
    # Update student's domain if provided
    student = db.query(models.Student).filter(models.Student.user_id == student_id).first()
    if student and domain:
        student.major = domain
        db.commit()
    
    db.refresh(new_thesis_defense)
    return new_thesis_defense


@router.get("/soutenance-requests", response_model=List[schemas.ThesisDefense])
def get_student_requests(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(require_student),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all soutenance requests for a specific student.
    """
    defenses = crud.thesis_defense.get_by_student(db=db, student_id=current_user.id, skip=skip, limit=limit)
    return defenses


@router.get("/dashboard", response_model=schemas.StudentDashboardStats)
def get_student_dashboard(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(require_student)
):
    """
    Get dashboard statistics for a student.
    """
    defenses = crud.thesis_defense.get_by_student(db=db, student_id=current_user.id)

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
    current_user: models.user.User = Depends(require_student)
):
    """
    Get details of a specific soutenance request.
    """
    defense = db.query(models.ThesisDefense).filter(models.ThesisDefense.id == defense_id).first()
    if not defense:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Ensure the request belongs to this student or the user is a manager/professor
    if defense.student_id != current_user.id and current_user.role in ['student']:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    
    return defense
