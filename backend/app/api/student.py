from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from pathlib import Path
import os
from uuid import uuid4

from .. import schemas, models
from .. import crud
from ..db.session import get_db
from ..dependencies import get_current_user, require_student

router = APIRouter(dependencies=[Depends(require_student)])

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


@router.post("/soutenance-requests", response_model=schemas.ThesisDefense)
async def create_soutenance_request(
    *,
    db: Session = Depends(get_db),
    title: str = Form(...),
    domain: str = Form(...),
    pdf: UploadFile = File(...),
    current_user: models.user.User = Depends(get_current_user)
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
    
    # TODO: Implement AI analysis for summary, domain detection, and similarity score
    # This would call your AI service here
    ai_summary = f"AI-generated summary for {title}. This will be implemented with actual AI integration."
    ai_domain = domain  # For now, use the domain provided by student
    ai_similarity_score = None  # Will be calculated by AI
    
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


@router.get("/soutenance-requests", response_model=List[schemas.ThesisDefense])
def get_student_requests(
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
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
    current_user: models.user.User = Depends(get_current_user)
):
    """
    Get dashboard statistics for a student.
    Returns count of pending, accepted, and refused requests.
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
    current_user: models.user.User = Depends(get_current_user)
):
    """
    Get details of a specific soutenance request.
    """
    defense = crud.thesis_defense.get(db=db, id=defense_id)
    if not defense:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Ensure the request belongs to this student
    if defense.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this request")
    
    return defense
