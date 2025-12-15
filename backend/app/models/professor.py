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

#######################################################3
# Ce qui doit être créé
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from ..models import ThesisDefense, JuryMember, Notification, Report
# from ..db.session import get_db

# router = APIRouter(prefix="/api/professors", tags=["professors"])

# # ✅ Endpoint 1: Voir toutes les soutenances assignées au professeur
# @router.get("/assigned-soutenances")
# async def get_assigned_soutenances(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     # Logique: Chercher toutes les ThesisDefense où le prof est dans JuryMember
#     pass

# # ✅ Endpoint 2: Voir détails d'une soutenance
# @router.get("/soutenances/{defense_id}")
# async def get_soutenance_detail(defense_id: int, ...):
#     # Retourner: defense + student info + report + jury members
#     pass

# # ✅ Endpoint 3: Télécharger le rapport PDF
# @router.get("/soutenances/{defense_id}/report/download")
# async def download_report(defense_id: int, ...):
#     # Retourner le fichier PDF
#     pass

# # ✅ Endpoint 4: Voir notifications
# @router.get("/notifications")
# async def get_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     # Retourner notifications du professeur non lues
#     pass

# # ✅ Endpoint 5: Marquer notification comme lue
# @router.patch("/notifications/{notification_id}/read")
# async def mark_notification_read(notification_id: int, ...):
#     pass