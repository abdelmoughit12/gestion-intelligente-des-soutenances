from sqlalchemy.orm import Session
from typing import List, Any
from ..models.user import User, UserRole
from ..models.professor import Professor
from ..schemas.professor import ProfessorCreateData
from ..core.security import get_password_hash

class CRUDProfessor:
    def get(self, db: Session, id: Any) -> Professor | None:
        return db.query(Professor).filter(Professor.user_id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Professor]:
        return db.query(Professor).offset(skip).limit(limit).all()

    def create_with_user(self, db: Session, *, obj_in: ProfessorCreateData) -> User:
        """
        Create a new professor user and the associated professor details.
        The user is created as active by default.
        """
        hashed_password = get_password_hash(obj_in.password)
        
        # Create the User object
        db_user = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            phone=obj_in.phone,
            role=UserRole.professor,
            is_active=True  # Professor account is active immediately
        )
        
        # Create the Professor details object
        db_professor_details = Professor(
            specialty=obj_in.specialty,
            user=db_user  # Associate with the User object
        )
        
        db.add(db_user)
        db.add(db_professor_details)
        db.commit()
        db.refresh(db_user)
        
        return db_user

professor = CRUDProfessor()
