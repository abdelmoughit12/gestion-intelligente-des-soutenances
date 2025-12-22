from app.db.session import SessionLocal, Base, engine
from app.models import (
    User, Professor, Student, ThesisDefense, JuryMember, 
    Report, Notification, UserRole, JuryRole, Manager
)
from app.core.security import get_password_hash
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
        existing_user = db.query(User).filter(User.email == 'manager@example.com').first()
        if existing_user:
            print("⚠️  Data already exists. Skipping seed.")
            return
        
        # 1️⃣ Créer les utilisateurs
        print("\n📝 Inserting users...")
        
        hashed_password = get_password_hash("password")

        manager_user = User(
            cni='CNI000000',
            last_name='Manager',
            first_name='Admin',
            email='manager@example.com',
            hashed_password=hashed_password,
            role=UserRole.manager,
            is_active=True
        )

        prof1_user = User(
            cni='CNI123456',
            last_name='El',
            first_name='Prof',
            email='prof1@example.com',
            hashed_password=hashed_password,
            role=UserRole.professor,
            is_active=True
        )
        
        prof2_user = User(
            cni='CNI222333',
            last_name='Prof2',
            first_name='Bob',
            email='prof2@example.com',
            hashed_password=hashed_password,
            role=UserRole.professor,
            is_active=True
        )
        
        student_user = User(
            cni='CNE987654',
            last_name='Student',
            first_name='Alice',
            email='student1@example.com',
            hashed_password=hashed_password,
            role=UserRole.student,
            is_active=True
        )
        
        db.add_all([manager_user, prof1_user, prof2_user, student_user])
        db.flush()  # Flush pour récupérer les IDs générés
        print(f"✅ Users created: Manager (id={manager_user.id}), Prof1 (id={prof1_user.id}), Prof2 (id={prof2_user.id}), Student (id={student_user.id})")

        # 2a️⃣ Créer le manager
        print("\n📝 Inserting manager details...")
        manager = Manager(user_id=manager_user.id)
        db.add(manager)
        db.flush()
        print(f"✅ Manager created.")
        
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
        
        # ... (rest of the script can remain the same)
        
        # Commit tous les changements
        db.commit()
        print("\n" + "="*60)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Summary:")
        print(f"  - Users: 4 (Manager, Prof1, Prof2, Student)")
        print(f"  - Password for all users: password")
        print(f"  - Professors: 2")
        print(f"  - Students: 1")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == '__main__':
    seed_database()
