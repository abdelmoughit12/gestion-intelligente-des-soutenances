from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from pathlib import Path
import os
from uuid import uuid4

from .. import schemas, models
from .. import crud
from ..services import ai
from ..db.session import get_db

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10MB
ALLOWED_PDF_CONTENT_TYPES = {"application/pdf", "application/x-pdf", "application/acrobat", "applications/vnd.pdf"}


def _sanitize_filename(filename: str) -> str:
    # Prevent path traversal and remove problematic characters
    name = Path(filename).name
    name = name.replace(" ", "_")
    keep = []
    for ch in name:
        if ch.isalnum() or ch in {"_", "-", "."}:
            keep.append(ch)
    sanitized = "".join(keep)
    return sanitized or "upload.pdf"


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
    if not pdf.filename or not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if pdf.content_type and pdf.content_type not in ALLOWED_PDF_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid PDF content type")

    # Save PDF file to disk (chunked, size-limited)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = _sanitize_filename(pdf.filename)
    unique_prefix = uuid4().hex
    safe_filename = f"{timestamp}_{unique_prefix}_{original_name}"
    rel_path = str(Path("uploads") / safe_filename).replace("\\", "/")
    abs_path = UPLOAD_DIR / safe_filename

    bytes_written = 0
    try:
        with open(abs_path, "wb") as buffer:
            while True:
                chunk = await pdf.read(1024 * 1024)
                if not chunk:
                    break
                bytes_written += len(chunk)
                if bytes_written > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="PDF file too large (max 10MB)")
                buffer.write(chunk)
    except HTTPException:
        if abs_path.exists():
            try:
                abs_path.unlink()
            except OSError:
                pass
        raise
    except Exception as e:
        if abs_path.exists():
            try:
                abs_path.unlink()
            except OSError:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        try:
            await pdf.close()
        except Exception:
            pass
    
    # AI (Gemini) with safe fallbacks - pass actual PDF path for text extraction
    import logging
    import json
    logger = logging.getLogger(__name__)
    
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


@router.get("/students/dashboard", response_model=schemas.StudentDashboardStats)
def get_student_dashboard(
    db: Session = Depends(get_db),
    student_id: int = 1,  # TODO: Get from authenticated user session
):
    """
    Get dashboard statistics for a student.
    Returns count of pending, accepted, and refused requests.
    """
    defenses = crud.thesis_defense.get_by_student(db=db, student_id=student_id)

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
