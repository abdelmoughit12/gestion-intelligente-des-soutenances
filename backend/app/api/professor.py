"""
 API Professeur - Endpoints pour le Dashboard

Ce fichier contient tous les endpoints que le frontend appelle:
- GET /api/professors/assigned-soutenances     → Liste des soutenances assignées
- GET /api/professors/soutenances/{id}         → Détails d'une soutenance
- GET /api/professors/soutenances/{id}/report/download → Télécharger PDF
- POST /api/professors/soutenances/{id}/evaluation    → Soumettre une évaluation
- GET /api/professors/notifications             → Lister les notifications
- PATCH /api/professors/notifications/{id}/read → Marquer comme lue
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import os

from ..models import (
    User, 
    Professor, 
    ThesisDefense, 
    JuryMember, 
    Student, 
    Report,
    Notification,
    ProfessorEvaluation
)
from .. import crud, schemas
from ..db.session import SessionLocal

router = APIRouter(prefix="/api/professors", tags=["professors"])


def get_db():
    
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close()  

def get_current_professor(
    x_professor_id: int = Header(..., description="ID du professeur pour test")
) -> dict:
    
    return {"id": x_professor_id, "role": "professor"}

@router.get("/", response_model=List[schemas.Professor])
def read_professors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all professors.
    """
    professors = crud.professor.get_multi(db, skip=skip, limit=limit)
    return professors

class AssignedSoutenanceSchema(BaseModel):
   
    id: int
    title: str
    studentName: str
    studentEmail: str
    domain: str
    status: str
    aiSummary: Optional[str] = None  
    aiSimilarityScore: Optional[float] = None
    scheduledDate: Optional[str] = None  
    scheduledTime: Optional[str] = None  
    juryRole: str
    
    class Config:
        from_attributes = True  


class EvaluationSubmitSchema(BaseModel):
    """
    Schema pour la soumission d'une évaluation.
    
    Utilisé par: EvaluationForm.tsx → POST /soutenances/{id}/evaluation
    
    Champs:
    - score: Note de 0 à 20
    - comments: Commentaires détaillés (minimum 10 caractères)
    """
    score: float = Field(..., ge=0, le=20, description="Score entre 0 et 20")
    comments: str = Field(..., description="Commentaires ")


class EvaluationResponseSchema(BaseModel):
    """Schema de réponse après soumission d'une évaluation."""
    success: bool
    message: str
    evaluation: Optional[dict] = None


class NotificationSchema(BaseModel):
    """
    Schema pour les notifications.
    
    Utilisé par: Endpoint 5 → GET /notifications
    
    Champs:
    - id: Identifiant unique de la notification
    - title: Titre de la notification
    - message: Contenu du message
    - is_read: Si la notification a été lue ou non
    - creation_date: Quand la notification a été créée
    """
    id: int
    title: str
    message: str
    is_read: bool
    creation_date: str  # ISO format datetime
    
    class Config:
        from_attributes = True


class NotificationReadSchema(BaseModel):
    success: bool
    message: str
    notification: Optional[NotificationSchema] = None

@router.get("/assigned-soutenances", response_model=List[AssignedSoutenanceSchema])
async def get_assigned_soutenances(
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> List[dict]:
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(
            status_code=401, 
            detail="Professeur non authentifié"
        )
    

    try:
        soutenances_data = db.query(
            ThesisDefense.id,
            ThesisDefense.title,
            ThesisDefense.status,
            ThesisDefense.defense_date,
            ThesisDefense.defense_time,

            func.concat(
                User.first_name,
                " ",
                User.last_name
            ).label("student_name"),  
            User.email.label("student_email"),  
            Student.major.label("domain"),
            
            Report.ai_summary,
            Report.ai_similarity_score,
            
            JuryMember.role.label("jury_role")
            
        ).join(

            JuryMember,
            JuryMember.thesis_defense_id == ThesisDefense.id
        ).join(
            Student,
            Student.user_id == ThesisDefense.student_id
        ).join(
            User,
            User.id == Student.user_id
        ).join(
            Report,
            Report.id == ThesisDefense.report_id,
            isouter=True
        ).filter(
            JuryMember.professor_id == professor_id
        ).all()  
        result = []
        for row in soutenances_data:
            result.append({
                "id": row.id,
                "title": row.title,
                "studentName": row.student_name,
                "studentEmail": row.student_email,
                "domain": row.domain,
                "status": row.status,
                "aiSummary": row.ai_summary,
                "aiSimilarityScore": row.ai_similarity_score,
                "scheduledDate": row.defense_date.isoformat() if row.defense_date else None,
                "scheduledTime": str(row.defense_time) if row.defense_time else None,
                "juryRole": row.jury_role.value if row.jury_role else None
            })
        
        return result
        
    except Exception as e:
        print(f" Erreur lors de la récupération des soutenances: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur: impossible de récupérer les soutenances"
        )



@router.get("/soutenances/{defense_id}", response_model=AssignedSoutenanceSchema)
async def get_soutenance_detail(
    defense_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    try:
        access_check = db.query(JuryMember).filter(
            and_(
                JuryMember.thesis_defense_id == defense_id,
                JuryMember.professor_id == professor_id
            )
        ).first()
        
        if not access_check:
            raise HTTPException(
                status_code=403,
                detail="Vous n'êtes pas assigné à cette soutenance"
            )
        
        soutenance_data = db.query(
            ThesisDefense.id,
            ThesisDefense.title,
            ThesisDefense.status,
            ThesisDefense.defense_date,
            ThesisDefense.defense_time,
            
            func.concat(
                User.first_name,
                " ",
                User.last_name
            ).label("student_name"),
            User.email.label("student_email"),
            Student.major.label("domain"),
            
            Report.ai_summary,
            Report.ai_similarity_score,
            
            JuryMember.role.label("jury_role")
            
        ).join(
            JuryMember,
            JuryMember.thesis_defense_id == ThesisDefense.id
        ).join(
            Student,
            Student.user_id == ThesisDefense.student_id
        ).join(
            User,
            User.id == Student.user_id
        ).join(
            Report,
            Report.id == ThesisDefense.report_id,
            isouter=True
        ).filter(
            ThesisDefense.id == defense_id
        ).first()
        
        if not soutenance_data:
            raise HTTPException(
                status_code=404,
                detail="Soutenance non trouvée"
            )
        
        return {
            "id": soutenance_data.id,
            "title": soutenance_data.title,
            "studentName": soutenance_data.student_name,
            "studentEmail": soutenance_data.student_email,
            "domain": soutenance_data.domain,
            "status": soutenance_data.status,
aiSummary: soutenance_data.ai_summary,
            "aiSimilarityScore": soutenance_data.ai_similarity_score,
            "scheduledDate": soutenance_data.defense_date.isoformat() if soutenance_data.defense_date else None,
            "scheduledTime": str(soutenance_data.defense_time) if soutenance_data.defense_time else None,
            "juryRole": soutenance_data.jury_role.value if soutenance_data.jury_role else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la récupération du détail: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur"
        )


@router.get("/soutenances/{defense_id}/report/download")
async def download_report(
    defense_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
):
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    
    try:
        access_check = db.query(JuryMember).filter(
            and_(
                JuryMember.thesis_defense_id == defense_id,
                JuryMember.professor_id == professor_id
            )
        ).first()
        
        if not access_check:
            raise HTTPException(
                status_code=403,
                detail="Vous n'êtes pas assigné à cette soutenance"
            )
        
        defense = db.query(ThesisDefense).filter(
            ThesisDefense.id == defense_id
        ).first()
        
        if not defense:
            raise HTTPException(
                status_code=404,
                detail="Soutenance non trouvée"
            )
        
        if not defense.report_id:
            raise HTTPException(
                status_code=404,
                detail="Aucun rapport disponible pour cette soutenance"
            )
        
        report = db.query(Report).filter(
            Report.id == defense.report_id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=404,
                detail="Rapport non trouvé"
            )
        
        report_path = os.path.join("storage", "reports", report.file_name)
        
        if not os.path.exists(report_path):
            print(f"⚠️  Fichier non trouvé: {report_path}")
            raise HTTPException(
                status_code=404,
                detail=f"Fichier du rapport non trouvé: {report.file_name}"
            )
        
        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename=f"report-defense-{defense_id}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors du téléchargement: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors du téléchargement"
        )



@router.post("/soutenances/{defense_id}/evaluation", response_model=EvaluationResponseSchema)
async def submit_evaluation(
    defense_id: int,
    evaluation_data: EvaluationSubmitSchema,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    
    try:
        access_check = db.query(JuryMember).filter(
            and_(
                JuryMember.thesis_defense_id == defense_id,
                JuryMember.professor_id == professor_id
            )
        ).first()
        
        if not access_check:
            raise HTTPException(
                status_code=403,
                detail="Vous n'êtes pas assigné à cette soutenance"
            )
        
        defense = db.query(ThesisDefense).filter(
            ThesisDefense.id == defense_id
        ).first()
        
        if not defense:
            raise HTTPException(
                status_code=404,
                detail="Soutenance non trouvée"
            )
        
        existing_evaluation = db.query(ProfessorEvaluation).filter(
            and_(
                ProfessorEvaluation.thesis_defense_id == defense_id,
                ProfessorEvaluation.professor_id == professor_id
            )
        ).first()
        
        
        if existing_evaluation:
            print(f"📝 Mise à jour de l'évaluation {existing_evaluation.id}")
            
            existing_evaluation.score = evaluation_data.score
            existing_evaluation.comments = evaluation_data.comments
            
            defense.status = 'evaluated'
            
            db.commit()
            
            return {
                "success": True,
                "message": "Évaluation mise à jour avec succès",
                "evaluation": {
                    "soutenanceId": defense_id,
                    "score": existing_evaluation.score,
                    "comments": existing_evaluation.comments,
                    "submittedAt": existing_evaluation.submission_date.isoformat()
                }
            }
        else:
            print(f"✍️  Création d'une nouvelle évaluation")
            
            new_evaluation = ProfessorEvaluation(
                thesis_defense_id=defense_id,
                professor_id=professor_id,
                score=evaluation_data.score,
                comments=evaluation_data.comments
            )
            
            db.add(new_evaluation)

            defense.status = 'evaluated'
            
            db.commit()
            db.refresh(new_evaluation)  
            
            return {
                "success": True,
                "message": "Évaluation soumise avec succès",
                "evaluation": {
                    "soutenanceId": defense_id,
                    "score": new_evaluation.score,
                    "comments": new_evaluation.comments,
                    "submittedAt": new_evaluation.submission_date.isoformat()
                }
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la soumission de l'évaluation: {str(e)}")
        db.rollback()  
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors de la soumission"
        )

@router.get("/notifications", response_model=List[NotificationSchema])
async def get_notifications(
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> List[dict]: 
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(
            status_code=401,
            detail="Professeur non authentifié"
        )
    
    try:
        notifications = db.query(Notification).filter(
            Notification.user_id == professor_id
        ).order_by(
            Notification.creation_date.desc()  
        ).all()
        
        return notifications
    
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des notifications: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors de la récupération des notifications"
        )


@router.patch("/notifications/{notification_id}/read", response_model=NotificationReadSchema)
async def mark_notification_read(
    notification_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
 
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(
            status_code=401,
            detail="Professeur non authentifié"
        )
    
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=404,
                detail=f"Notification {notification_id} non trouvée"
            )
        
        if notification.user_id != professor_id:
            raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas accès à cette notification"
            )
        
        notification.is_read = True
        
        db.commit()
        
        db.refresh(notification)
        
        return {
            "success": True,
            "message": "Notification marquée comme lue",
            "notification": notification  
        }
    
    except HTTPException:
        raise  
    
    except Exception as e:
        print(f"❌ Erreur lors du marquage de notification: {str(e)}")
        db.rollback()  # Annuler tout changement en cas d'erreur
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors du marquage de notification"
        )
