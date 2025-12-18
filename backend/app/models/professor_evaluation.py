"""
 Modèle ProfessorEvaluation

Ce modèle représente une évaluation soumise par un professeur pour une soutenance.
Il stocke:
- Le score de la soutenance (0-20)
- Les commentaires du professeur
- La date d'évaluation
- Qui a évalué (professor_id)
- Quelle soutenance a été évaluée (thesis_defense_id)
"""

from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base


class ProfessorEvaluation(Base):
    """
    Table: professor_evaluations
    
    Stocke les évaluations des professeurs pour les soutenances.
    Chaque professeur ne peut évaluer une soutenance qu'une seule fois.
    """
    
    __tablename__ = "professor_evaluations"
    
    # ===== COLONNES =====
    
    id = Column(
        Integer, 
        primary_key=True,      
        index=True,            
        autoincrement=True     
    )
    
    thesis_defense_id = Column(
        Integer,
        ForeignKey(
            "thesis_defenses.id",  
            ondelete="CASCADE",   
            onupdate="CASCADE"     
        ),
        nullable=False         
    )
    
    professor_id = Column(
        Integer,
        ForeignKey(
            "professors.user_id",  
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        nullable=False         
    )
    
    score = Column(
        Float,                 
        nullable=False        
        
    )
    
    comments = Column(
        Text,                  
        nullable=True        
    )
    
    submission_date = Column(
        DateTime,
        server_default=func.now(), 
        nullable=False
    )
    

    __table_args__ = (
        UniqueConstraint(
            'thesis_defense_id',
            'professor_id',
            name='unique_prof_eval_per_defense'
        ),
    )
    
    
    thesis_defense = relationship(
        "ThesisDefense",       
        backref="evaluations"  
    )
    
    professor = relationship(
        "Professor",
        backref="evaluations"
    )
    
    
    def __repr__(self):
        return (
            f"<ProfessorEvaluation("
            f"id={self.id}, "
            f"defense_id={self.thesis_defense_id}, "
            f"professor_id={self.professor_id}, "
            f"score={self.score}"
            f")>"
        )


