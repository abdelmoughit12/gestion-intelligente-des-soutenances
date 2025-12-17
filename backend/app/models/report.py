from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # "ID_Rapport"
    file_name = Column(String(255), nullable=False) # "Nom_Fichier"
    ai_summary = Column(Text, nullable=True) # "Resume_IA"
    ai_domain = Column(String(150), nullable=True) # "Domaine_IA"
    ai_similarity_score = Column(Float, nullable=True) # "Score_Similarite_IA"
    student_id = Column(Integer, ForeignKey("students.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True) # "D_Utilisateur" -> fk_rapport_etudiant
    submission_date = Column(DateTime, server_default=func.now()) # "Date_depot"

    # Relationship back to Student
    student = relationship("Student", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, file_name='{self.file_name}')>"
