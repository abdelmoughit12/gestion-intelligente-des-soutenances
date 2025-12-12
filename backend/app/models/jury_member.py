from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base
import enum

class JuryRole(str, enum.Enum):
    president = "president"
    member = "member"
    secretary = "secretary"
    examiner = "examiner"

class JuryMember(Base):
    __tablename__ = "jury_members"

    thesis_defense_id = Column(Integer, ForeignKey("thesis_defenses.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    professor_id = Column(Integer, ForeignKey("professors.user_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    role = Column(SQLAlchemyEnum(JuryRole), default=JuryRole.member) # "Role_dans_jury"

    # Relationships
    thesis_defense = relationship("ThesisDefense", back_populates="jury_members")
    professor = relationship("Professor", back_populates="jury_assignments")

    def __repr__(self):
        return f"<JuryMember(defense_id={self.thesis_defense_id}, professor_id={self.professor_id})>"
