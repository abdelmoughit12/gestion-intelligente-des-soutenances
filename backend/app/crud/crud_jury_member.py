from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import models, schemas

class CRUDJuryMember:
    def __init__(self, model: type[models.JuryMember]):
        self.model = model

    def create(self, db: Session, *, obj_in: schemas.JuryMemberCreate) -> models.JuryMember:
        """
        Create a new jury member assignment.
        """
        db_obj = self.model(
            thesis_defense_id=obj_in.thesis_defense_id,
            professor_id=obj_in.professor_id,
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_defense(self, db: Session, *, defense_id: int) -> List[models.JuryMember]:
        """
        Get all jury members for a specific thesis defense.
        """
        return (
            db.query(self.model)
            .filter(self.model.thesis_defense_id == defense_id)
            .options(joinedload(self.model.professor).joinedload(models.Professor.user)) # Eager load professor and user details
            .all()
        )

    def get(self, db: Session, *, thesis_defense_id: int, professor_id: int) -> models.JuryMember | None:
        """
        Get a specific jury member by thesis_defense_id and professor_id.
        """
        return db.query(self.model).filter(
            self.model.thesis_defense_id == thesis_defense_id,
            self.model.professor_id == professor_id
        ).first()

    def update(
        self, db: Session, *, db_obj: models.JuryMember, obj_in: schemas.JuryMemberUpdate
    ) -> models.JuryMember:
        """
        Update a jury member.
        """
        if obj_in.professor_id is not None:
            db_obj.professor_id = obj_in.professor_id
        if obj_in.role is not None:
            db_obj.role = obj_in.role

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

jury_member = CRUDJuryMember(models.JuryMember)
