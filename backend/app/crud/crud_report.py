from typing import Optional
from sqlalchemy.orm import Session
from ..models.report import Report
from ..schemas.report import ReportCreate, ReportUpdate


def get(db: Session, id: int) -> Optional[Report]:
    """Get a report by ID"""
    return db.query(Report).filter(Report.id == id).first()


def get_multi(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple reports"""
    return db.query(Report).offset(skip).limit(limit).all()


def get_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    """Get all reports for a specific student"""
    return db.query(Report).filter(Report.student_id == student_id).offset(skip).limit(limit).all()


def create(db: Session, obj_in: ReportCreate) -> Report:
    """Create a new report"""
    db_obj = Report(
        file_name=obj_in.file_name,
        ai_summary=obj_in.ai_summary,
        ai_domain=obj_in.ai_domain,
        ai_similarity_score=obj_in.ai_similarity_score,
        student_id=obj_in.student_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Report, obj_in: ReportUpdate) -> Report:
    """Update a report"""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int) -> Report:
    """Delete a report"""
    obj = db.query(Report).get(id)
    db.delete(obj)
    db.commit()
    return obj
