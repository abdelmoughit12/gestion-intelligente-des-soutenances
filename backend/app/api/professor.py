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
from ..db.session import SessionLocal

# ===== CONFIGURATION DU ROUTER =====
router = APIRouter(prefix="/api/professors", tags=["professors"])

# ===== DÉPENDANCES =====

def get_db():
    """
    Dépendance qui fournit une session de base de données.
    
    Comment ça marche:
    1. FastAPI appelle cette fonction
    2. Elle crée une session DB
    3. La fonction yield la session
    4. FastAPI passe la session à l'endpoint
    5. Après l'endpoint, le finally ferme la session
    """
    db = SessionLocal()
    try:
        yield db  # "yield" = pause ici et donne la session à l'endpoint
    finally:
        db.close()  # Fermer la session après

def get_current_professor(
    x_professor_id: int = Header(..., description="ID du professeur pour test")
) -> dict:
    
    return {"id": x_professor_id, "role": "professor"}




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
    comments: str = Field(..., min_length=10, description="Commentaires minimum 10 caractères")


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
    """
    Schema de réponse après marquer une notification comme lue.
    
    Utilisé par: Endpoint 6 → PATCH /notifications/{id}/read
    """
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


# ===== ENDPOINT 2: GET /api/professors/soutenances/{id} =====

@router.get("/soutenances/{defense_id}", response_model=AssignedSoutenanceSchema)
async def get_soutenance_detail(
    defense_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
    """
    📄 Récupère les détails d'une soutenance spécifique.
    
    Utilisé par: SoutenanceDetailsModal.tsx
    
    Sécurité: Vérifie que le professeur actuel est assigné à cette soutenance
    """
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    
    try:
        # ÉTAPE 1: Vérifier l'accès (SÉCURITÉ)
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
        
        # ÉTAPE 2: Récupérer les détails
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
            "aiSummary": soutenance_data.ai_summary,
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


# ===== ENDPOINT 3: GET /api/professors/soutenances/{id}/report/download =====

@router.get("/soutenances/{defense_id}/report/download")
async def download_report(
    defense_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
):
    """
    📥 Télécharge le rapport PDF d'une soutenance.
    
    Utilisé par: SoutenanceDetailsModal.tsx → Bouton "Download Report"
    
    Processus:
    1. Vérifier que le prof est assigné à cette soutenance
    2. Récupérer le fichier PDF de la BD
    3. Vérifier que le fichier existe sur le disque
    4. Retourner le fichier via FileResponse
    
    FileResponse expliqué:
    - Retourne un fichier au lieu de JSON
    - Frontend le télécharge automatiquement
    - Le header Content-Type indique le type (PDF, image, etc.)
    """
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    
    try:
        # ÉTAPE 1: Vérifier l'accès (même que Endpoint 2)
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
        
        # ÉTAPE 2: Récupérer la soutenance et son rapport
        defense = db.query(ThesisDefense).filter(
            ThesisDefense.id == defense_id
        ).first()
        
        if not defense:
            raise HTTPException(
                status_code=404,
                detail="Soutenance non trouvée"
            )
        
        # ÉTAPE 3: Vérifier qu'il y a un rapport
        if not defense.report_id:
            raise HTTPException(
                status_code=404,
                detail="Aucun rapport disponible pour cette soutenance"
            )
        
        # ÉTAPE 4: Récupérer le fichier du rapport
        report = db.query(Report).filter(
            Report.id == defense.report_id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=404,
                detail="Rapport non trouvé"
            )
        
        # ÉTAPE 5: Construire le chemin du fichier
        # Les fichiers sont stockés dans: backend/storage/reports/
        # Exemple: backend/storage/reports/report_1_defense_5.pdf
        
        report_path = os.path.join("storage", "reports", report.file_name)
        
        # ÉTAPE 6: Vérifier que le fichier existe
        if not os.path.exists(report_path):
            print(f"⚠️  Fichier non trouvé: {report_path}")
            raise HTTPException(
                status_code=404,
                detail=f"Fichier du rapport non trouvé: {report.file_name}"
            )
        
        # ÉTAPE 7: Retourner le fichier
        # FileResponse:
        # - path: le chemin du fichier sur le disque
        # - media_type: le type MIME (application/pdf pour PDF)
        # - filename: le nom du fichier pour le téléchargement
        
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


# ===== ENDPOINT 4: POST /api/professors/soutenances/{id}/evaluation =====

@router.post("/soutenances/{defense_id}/evaluation", response_model=EvaluationResponseSchema)
async def submit_evaluation(
    defense_id: int,
    evaluation_data: EvaluationSubmitSchema,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
    """
    📝 Soumet une évaluation pour une soutenance.
    
    Utilisé par: EvaluationForm.tsx → Bouton "Soumettre l'Évaluation"
    
    Processus:
    1. Recevoir les données du frontend (score + commentaires)
    2. Les valider (score 0-20, commentaires min 10 chars)
    3. Vérifier que le prof peut évaluer cette soutenance
    4. Chercher si une évaluation existe déjà
    5. Si OUI: UPDATE
    6. Si NON: INSERT (CREATE)
    7. Retourner: succès + détails
    
    Différence avec Endpoint 3:
    - Endpoint 3: GET (récupérer)
    - Endpoint 4: POST (créer/modifier)
    
    Différence avec Endpoint 1-3:
    - Endpoint 1-3: Pas de modification BD
    - Endpoint 4: Modifie la BD (INSERT/UPDATE)
    """
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(status_code=401, detail="Professeur non authentifié")
    
    try:
        # ÉTAPE 1: Vérifier l'accès
        # Le prof doit être assigné à cette soutenance pour pouvoir l'évaluer
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
        
        # ÉTAPE 2: Vérifier que la soutenance existe
        defense = db.query(ThesisDefense).filter(
            ThesisDefense.id == defense_id
        ).first()
        
        if not defense:
            raise HTTPException(
                status_code=404,
                detail="Soutenance non trouvée"
            )
        
        # ÉTAPE 3: Validation des données
        # Pydantic valide déjà:
        #   - 0 <= score <= 20 (Field(..., ge=0, le=20))
        #   - len(comments) >= 10 (Field(..., min_length=10))
        # Mais on peut ajouter de la logique custom si nécessaire
        
        # Exemple de logique custom:
        # if evaluation_data.score < 0 or evaluation_data.score > 20:
        #     raise HTTPException(...)
        
        # ÉTAPE 4: Chercher si une évaluation existe déjà
        # Uniqueness constraint: (thesis_defense_id, professor_id)
        
        existing_evaluation = db.query(ProfessorEvaluation).filter(
            and_(
                ProfessorEvaluation.thesis_defense_id == defense_id,
                ProfessorEvaluation.professor_id == professor_id
            )
        ).first()
        
        # ÉTAPE 5: INSERT ou UPDATE
        
        if existing_evaluation:
            # UPDATE: La évaluation existe déjà, on la modifie
            print(f"📝 Mise à jour de l'évaluation {existing_evaluation.id}")
            
            existing_evaluation.score = evaluation_data.score
            existing_evaluation.comments = evaluation_data.comments
            
            # Mettre à jour le statut de la soutenance
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
            # INSERT: C'est la première évaluation
            print(f"✍️  Création d'une nouvelle évaluation")
            
            new_evaluation = ProfessorEvaluation(
                thesis_defense_id=defense_id,
                professor_id=professor_id,
                score=evaluation_data.score,
                comments=evaluation_data.comments
                # submission_date rempli automatiquement par PostgreSQL
            )
            
            db.add(new_evaluation)

            # Mettre à jour le statut de la soutenance
            defense.status = 'evaluated'
            
            db.commit()
            db.refresh(new_evaluation)  # Rafraîchir pour avoir les valeurs générées
            
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
        db.rollback()  # Annuler tout changement en cas d'erreur
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors de la soumission"
        )


# ===== ENDPOINT 5: GET /notifications =====

@router.get("/notifications", response_model=List[NotificationSchema])
async def get_notifications(
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Récupérer toutes les notifications du professeur connecté.
    
    CONCEPT 1: Query avec ORDER BY
    ================================
    Jusqu'à présent, on a:
    - db.query(...).filter(...).all() → liste non triée
    
    Maintenant on ajoute:
    - .order_by(Notification.creation_date.desc()) → trier par date décroissante
    
    Résultat:
    - Les notifications les plus récentes apparaissent en premier
    
    Exemple:
    db.query(Notification) \
        .filter(Notification.user_id == 1) \
        .order_by(Notification.creation_date.desc()) \
        .all()
    
    SQL généré:
    SELECT * FROM notifications 
    WHERE user_id = 1 
    ORDER BY creation_date DESC;
    
    CONCEPT 2: Filtrage sans JOIN
    ===============================
    Cette fois, on requête une seule table (Notification)
    
    Avantage: Plus simple que les JOINs complexes
    Désavantage: On ne peut pas accéder aux données liées (ex: soutenance details)
    
    CONCEPT 3: List[NotificationSchema]
    ====================================
    response_model=List[NotificationSchema] indique:
    - FastAPI va valider chaque notification
    - Convertir chaque ligne en NotificationSchema
    - Retourner une liste JSON valide
    """
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(
            status_code=401,
            detail="Professeur non authentifié"
        )
    
    try:
        # Query la table Notification filtrée par user_id et triée par date
        notifications = db.query(Notification).filter(
            Notification.user_id == professor_id
        ).order_by(
            Notification.creation_date.desc()  # DESC = décroissant (récent en premier)
        ).all()
        
        return notifications
    
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des notifications: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors de la récupération des notifications"
        )


# ===== ENDPOINT 6: PATCH /notifications/{id}/read =====

@router.patch("/notifications/{notification_id}/read", response_model=NotificationReadSchema)
async def mark_notification_read(
    notification_id: int,
    current_user: dict = Depends(get_current_professor),
    db: Session = Depends(get_db)
) -> dict:
    """
    Marquer une notification comme lue.
    
    CONCEPT 1: PATCH vs PUT vs POST
    ================================
    
    POST: Créer une nouvelle ressource
    - POST /notifications {"title": "..."} → Crée une notification
    
    PUT: Remplacer ENTIÈREMENT une ressource
    - PUT /notifications/1 {"title": "New", "message": "New msg", ...} → Remplace tous les champs
    
    PATCH: Modifier PARTIELLEMENT une ressource
    - PATCH /notifications/1 → Modifie juste is_read = True, laisse autres champs intacts
    
    Avantage de PATCH:
    - Client ne doit pas envoyer tous les champs
    - Seulement les champs à modifier
    - Plus efficace et moins d'erreurs
    
    CONCEPT 2: Vérification de propriété
    =====================================
    Avant de modifier une notification:
    1. Chercher la notification
    2. Vérifier que notification.user_id == current_user.id
    3. Modifier seulement si elle appartient au user connecté
    
    Sinon: Risque de sécurité!
    Exemple: User 1 modifie notification de User 2?
    
    Codes:
    - 404: Notification n'existe pas
    - 403: Notification appartient à quelqu'un d'autre
    - 200: Success
    
    CONCEPT 3: UPDATE avec .filter() et modification
    ================================================
    SQLAlchemy offre 2 façons de modifier:
    
    Façon 1 (que nous utilisons - simple):
    notification = db.query(...).filter(...).first()
    notification.is_read = True
    db.commit()
    
    Façon 2 (directe - bulk update):
    db.query(...).filter(...).update({Notification.is_read: True})
    db.commit()
    
    Nous préférons Façon 1 car:
    - Plus lisible
    - On récupère l'objet pour le retourner
    - Plus facile à debugger
    """
    
    professor_id = current_user.get("id")
    if not professor_id:
        raise HTTPException(
            status_code=401,
            detail="Professeur non authentifié"
        )
    
    try:
        # Chercher la notification
        notification = db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        # Vérifier qu'elle existe
        if not notification:
            raise HTTPException(
                status_code=404,
                detail=f"Notification {notification_id} non trouvée"
            )
        
        # Vérifier que c'est la notification du professeur connecté
        if notification.user_id != professor_id:
            raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas accès à cette notification"
            )
        
        # Modifier la notification
        notification.is_read = True
        
        # Sauvegarder en base de données
        db.commit()
        
        # Rafraîchir pour avoir les données à jour
        db.refresh(notification)
        
        # Retourner la réponse
        return {
            "success": True,
            "message": "Notification marquée comme lue",
            "notification": notification  # Retourner la notification modifiée
        }
    
    except HTTPException:
        raise  # Relancer les exceptions HTTP (404, 403, 401)
    
    except Exception as e:
        print(f"❌ Erreur lors du marquage de notification: {str(e)}")
        db.rollback()  # Annuler tout changement en cas d'erreur
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors du marquage de notification"
        )

