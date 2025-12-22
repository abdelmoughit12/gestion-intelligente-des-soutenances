from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base
import enum

class UserRole(str, enum.Enum):
    student = "student"
    professor = "professor"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cni = Column(String(20), unique=True, nullable=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=False)
    creation_date = Column(DateTime, server_default=func.now())

    # Relationships
    student_details = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    professor_details = relationship("Professor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    manager_details = relationship("Manager", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
