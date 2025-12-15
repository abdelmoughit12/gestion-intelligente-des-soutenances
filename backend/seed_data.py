"""
Script de seed pour insérer des données de test dans la base de données.
Usage: python seed_data.py
"""

from app.db.session import SessionLocal, Base, engine
from app.models import (
    User, Professor, Student, ThesisDefense, JuryMember, 
    Report, Notification, UserRole, JuryRole
)
from datetime import datetime, date, time

def seed_database():
    """Insert test data into the database."""
    
    # Créer les tables (au cas où)
    print("🔨 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created/verified")
    
    db = SessionLocal()
    
    try:
        # Vérifier si les données existent déjà
        existing_user = db.query(User).filter(User.email == 'prof1@example.com').first()
        if existing_user:
            print("⚠️  Data already exists. Skipping seed.")
            return
        
        # 1️⃣ Créer les utilisateurs
        print("\n📝 Inserting users...")
        
        prof1_user = User(
            cni='CNI123456',
            last_name='El',
            first_name='Prof',
            email='prof1@example.com',
            hashed_password='hashed_password_1',
            role=UserRole.professor
        )
        
        prof2_user = User(
            cni='CNI222333',
            last_name='Prof2',
            first_name='Bob',
            email='prof2@example.com',
            hashed_password='hashed_password_2',
            role=UserRole.professor
        )
        
        student_user = User(
            cni='CNE987654',
            last_name='Student',
            first_name='Alice',
            email='student1@example.com',
            hashed_password='hashed_password_3',
            role=UserRole.student
        )
        
        db.add_all([prof1_user, prof2_user, student_user])
        db.flush()  # Flush pour récupérer les IDs générés
        print(f"✅ Users created: Prof1 (id={prof1_user.id}), Prof2 (id={prof2_user.id}), Student (id={student_user.id})")
        
        # 2️⃣ Créer les professeurs
        print("\n📝 Inserting professors...")
        
        prof1 = Professor(user_id=prof1_user.id, specialty='Machine Learning')
        prof2 = Professor(user_id=prof2_user.id, specialty='Distributed Systems')
        
        db.add_all([prof1, prof2])
        db.flush()
        print(f"✅ Professors created: Prof1, Prof2")
        
        # 3️⃣ Créer l'étudiant
        print("\n📝 Inserting students...")
        
        student = Student(
            user_id=student_user.id,
            major='Computer Science',
            cne='CNE2025001',
            year=5
        )
        
        db.add(student)
        db.flush()
        print(f"✅ Student created: Alice")
        
        # 4️⃣ Créer les rapports
        print("\n📝 Inserting reports...")
        
        report1 = Report(
            file_name='sample_report.pdf',
            ai_summary='Résumé IA: Excellent travail sur le projet cloud avec IA.',
            ai_domain='AI',
            ai_similarity_score=0.12,
            student_id=student_user.id
        )
        
        db.add(report1)
        db.flush()
        print(f"✅ Report created: sample_report.pdf (id={report1.id})")
        
        # 5️⃣ Créer les soutenances
        print("\n📝 Inserting thesis defenses...")
        
        defense1 = ThesisDefense(
            student_id=student_user.id,
            title='AI-Powered Cloud',
            description='Projet sur l\'intégration de l\'IA dans les services cloud',
            status='scheduled',
            defense_date=date(2025, 12, 20),
            defense_time=time(10, 0, 0),
            report_id=report1.id
        )
        
        db.add(defense1)
        db.flush()
        print(f"✅ Thesis defense created: AI-Powered Cloud (id={defense1.id})")
        
        # 6️⃣ Créer les jury members
        print("\n📝 Inserting jury members...")
        
        jury1 = JuryMember(
            thesis_defense_id=defense1.id,
            professor_id=prof1_user.id,
            role=JuryRole.president
        )
        
        jury2 = JuryMember(
            thesis_defense_id=defense1.id,
            professor_id=prof2_user.id,
            role=JuryRole.member
        )
        
        db.add_all([jury1, jury2])
        db.flush()
        print(f"✅ Jury members created: Prof1 (president), Prof2 (member)")
        
        # 7️⃣ Créer les notifications
        print("\n📝 Inserting notifications...")
        
        notif1 = Notification(
            user_id=prof1_user.id,
            title='Soutenance assignée',
            message='Vous avez été assigné à la soutenance AI-Powered Cloud',
            action_type='assignment',
            is_read=False,
            creation_date=datetime(2025, 12, 15, 9, 0, 0)
        )
        
        notif2 = Notification(
            user_id=prof1_user.id,
            title='Rapport reçu',
            message='Le rapport pour AI-Powered Cloud a été déposé',
            action_type='report',
            is_read=False,
            creation_date=datetime(2025, 12, 14, 18, 30, 0)
        )
        
        notif3 = Notification(
            user_id=prof2_user.id,
            title='Nouvelle soutenance',
            message='Vous avez une nouvelle soutenance à évaluer',
            action_type='assignment',
            is_read=False,
            creation_date=datetime(2025, 12, 15, 10, 0, 0)
        )
        
        db.add_all([notif1, notif2, notif3])
        db.flush()
        print(f"✅ Notifications created: 3 notifications")
        
        # Commit tous les changements
        db.commit()
        print("\n" + "="*60)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Summary:")
        print(f"  - Users: 3 (Prof1, Prof2, Student)")
        print(f"  - Professors: 2")
        print(f"  - Students: 1")
        print(f"  - Reports: 1")
        print(f"  - Thesis Defenses: 1")
        print(f"  - Jury Members: 2")
        print(f"  - Notifications: 3")
        print("\n🎯 Test data ready for Postman!")
        print("\n💡 Recommended tests:")
        print("   1. GET /assigned-soutenances (Prof ID: 1)")
        print("   2. GET /soutenances/1 (Prof ID: 1)")
        print("   3. POST /soutenances/1/evaluation (Prof ID: 1)")
        print("   4. GET /notifications (Prof ID: 1)")
        print("   5. PATCH /notifications/1/read (Prof ID: 1)")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == '__main__':
    seed_database()
