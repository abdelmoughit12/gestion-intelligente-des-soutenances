from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..models.student import Student
from ..schemas.user import StudentRegistration
from ..core.security import get_password_hash

def get_user_by_cni(db: Session, cni: str) -> User | None:
    """
    Fetch a user by their CNI.
    """
    return db.query(User).filter(User.cni == cni).first()

def get_student_by_cne(db: Session, cne: str) -> Student | None:
    """
    Fetch a student by their CNE.
    """
    return db.query(Student).filter(Student.cne == cne).first()

def create_student_registration(db: Session, student_in: StudentRegistration) -> User:
    """
    Create a new student user with an associated student_details entry.
    The user is created as inactive by default.
    """
    hashed_password = get_password_hash(student_in.password)
    
    # Create the User object
    db_user = User(
        email=student_in.email,
        hashed_password=hashed_password,
        first_name=student_in.first_name,
        last_name=student_in.last_name,
        cni=student_in.cni,
        phone=student_in.phone,
        role=UserRole.student,
        is_active=False  # The account is inactive until approved by a manager
    )
    
    # Create the Student details object
    db_student_details = Student(
        cne=student_in.cne,
        user=db_user  # Associate with the User object
    )
    
    db.add(db_user)
    db.add(db_student_details)
    db.commit()
    db.refresh(db_user)
    
    return db_user
