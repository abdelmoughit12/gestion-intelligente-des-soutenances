from sqlalchemy.orm import Session
from typing import List, Any

from .. import models

class CRUDProfessor:
    def __init__(self, model: type[models.Professor]):
        self.model = model

    def get(self, db: Session, id: Any) -> models.Professor | None:
        # Professor's ID is the user_id, which is the primary key of the professors table
        return db.query(self.model).filter(self.model.user_id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[models.Professor]:
        return db.query(self.model).offset(skip).limit(limit).all()

professor = CRUDProfessor(models.Professor)
