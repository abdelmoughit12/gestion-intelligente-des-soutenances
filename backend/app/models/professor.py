from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Professor(Base):
    __tablename__ = "professors"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    specialty = Column(String(120), nullable=True) 

    user = relationship("User", back_populates="professor_details")
    jury_assignments = relationship("JuryMember", back_populates="professor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Professor(user_id={self.user_id}, specialty='{self.specialty}')>"

