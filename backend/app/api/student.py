from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil

from ..models import (
    ThesisDefense,
    Report,
    Student
)
from ..db.session import SessionLocal

router = APIRouter(prefix="/api/students", tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/soutenance-requests")
async def submit_soutenance_request(
    title: str = Form(...),
    domain: str = Form(...),
    pdf: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # For now, we'll use a hardcoded student_id. In a real app, this would come from the authenticated user.
    student_id = 1

    # Define the storage path for the report
    storage_path = os.path.join("storage", "reports")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    # Generate a unique filename
    file_extension = os.path.splitext(pdf.filename)[1]
    new_filename = f"report_student_{student_id}_{title.replace(' ', '_')}{file_extension}"
    file_location = os.path.join(storage_path, new_filename)

    # Save the uploaded file
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(pdf.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create a new Report record
    new_report = Report(
        file_name=new_filename,
        file_path=file_location,
        # These fields can be populated by an AI service later
        # ai_summary="Summary will be generated.",
        # ai_similarity_score=0.0
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    # Create a new ThesisDefense record
    new_thesis_defense = ThesisDefense(
        title=title,
        student_id=student_id,
        report_id=new_report.id,
        status="pending"  # Initial status
    )
    db.add(new_thesis_defense)
    db.commit()
    db.refresh(new_thesis_defense)

    return {
        "id": new_thesis_defense.id,
        "title": new_thesis_defense.title,
        "status": new_thesis_defense.status,
        "pdfUrl": f"/reports/{new_filename}", # This URL needs to be served by the backend
        "summary": new_report.ai_summary,
        "similarityScore": new_report.ai_similarity_score
    }
