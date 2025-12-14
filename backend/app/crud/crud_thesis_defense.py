from typing import Any, Dict, Union, List
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

from .. import models, schemas
from ..db.session import Base

class CRUDThesisDefense:
    def __init__(self, model: type[models.ThesisDefense]):
        self.model = model

    def get(self, db: Session, id: Any) -> models.ThesisDefense | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[models.ThesisDefense]:
        return (
            db.query(self.model)
            .options(
                joinedload(self.model.student).joinedload(models.Student.user),
                joinedload(self.model.report),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_student(self, db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[models.ThesisDefense]:
        """Get all thesis defenses for a specific student"""
        return (
            db.query(self.model)
            .options(
                joinedload(self.model.student).joinedload(models.Student.user),
                joinedload(self.model.report),
            )
            .filter(self.model.student_id == student_id)
            .order_by(self.model.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: schemas.ThesisDefenseCreate) -> models.ThesisDefense:
        """Create a new thesis defense"""
        db_obj = self.model(
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            student_id=obj_in.student_id,
            report_id=obj_in.report_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: models.ThesisDefense,
        obj_in: Union[schemas.ThesisDefenseUpdate, Dict[str, Any]]
    ) -> models.ThesisDefense:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Create an instance of the CRUD class to be used in API routes
thesis_defense = CRUDThesisDefense(models.ThesisDefense)
