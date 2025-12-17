from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Student(Base):
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    major = Column(String(250), nullable=True) # "Filiere"
    cne = Column(String(50), unique=True, nullable=True)
    year = Column(Integer, nullable=True) # "Annee"

    # Relationship back to User
    user = relationship("User", back_populates="student_details")
    reports = relationship("Report", back_populates="student")
    defenses = relationship("ThesisDefense", back_populates="student")

    def __repr__(self):
        return f"<Student(user_id={self.user_id}, cne='{self.cne}')>"
