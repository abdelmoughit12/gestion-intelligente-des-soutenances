from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class ThesisDefense(Base):
    __tablename__ = "thesis_defenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # "ID_Soutenance"
    student_id = Column(Integer, ForeignKey("students.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False) # "ID_Etudiant"
    title = Column(String(350), nullable=False) # "Titre"
    description = Column(Text, nullable=True) # "Description"
    status = Column(String(150), nullable=True) # "Statut"
    defense_date = Column(Date, nullable=True) # "Date_Soutenance"
    defense_time = Column(Time, nullable=True) # "Heure_Soutenance"
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="SET NULL", onupdate="CASCADE"), unique=True, nullable=True) # "ID_Rapport"

    # Relationships
    student = relationship("Student", back_populates="defenses")
    report = relationship("Report", backref="thesis_defense", uselist=False)
    jury_members = relationship("JuryMember", back_populates="thesis_defense", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ThesisDefense(id={self.id}, title='{self.title}')>"
