"""
Comprehensive seed script to populate database with test data for manager dashboard
Run: docker compose exec backend python scripts/seed_comprehensive_data.py
"""

import sys
import os
from datetime import datetime, date, time, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, Base, engine
from app.models import (
    User, Professor, Student, ThesisDefense, JuryMember,
    Report, Notification, UserRole, JuryRole
)
from app.core.security import get_password_hash

def seed_comprehensive_data():
    """Insert comprehensive test data into the database."""
    
    print("🔨 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created/verified\n")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_defense = db.query(ThesisDefense).first()
        if existing_defense:
            print("⚠️  Thesis defense data already exists.")
            response = input("Do you want to add more data anyway? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed.")
                return
        
        # Get existing users or create them
        print("📝 Checking/Creating users...")
        
        # Get or create students
        students_data = [
            {"email": "student@example.com", "first_name": "Alice", "last_name": "Student", "cni": "ST001", "major": "Computer Science", "cne": "CNE2024001", "year": 5},
            {"email": "bob.student@example.com", "first_name": "Bob", "last_name": "Martin", "cni": "ST002", "major": "Data Science", "cne": "CNE2024002", "year": 5},
            {"email": "carol.student@example.com", "first_name": "Carol", "last_name": "White", "cni": "ST003", "major": "AI & ML", "cne": "CNE2024003", "year": 5},
            {"email": "david.student@example.com", "first_name": "David", "last_name": "Brown", "cni": "ST004", "major": "Cybersecurity", "cne": "CNE2024004", "year": 5},
        ]
        
        student_users = []
        for s_data in students_data:
            user = db.query(User).filter(User.email == s_data["email"]).first()
            if not user:
                user = User(
                    cni=s_data["cni"],
                    last_name=s_data["last_name"],
                    first_name=s_data["first_name"],
                    email=s_data["email"],
                    hashed_password=get_password_hash("password"),
                    role=UserRole.student
                )
                db.add(user)
                db.flush()
                print(f"✅ Created user: {user.email}")
            
            # Check if Student record exists
            student = db.query(Student).filter(Student.user_id == user.id).first()
            if not student:
                student = Student(
                    user_id=user.id,
                    major=s_data["major"],
                    cne=s_data["cne"],
                    year=s_data["year"]
                )
                db.add(student)
                print(f"✅ Created student record for: {user.email}")
            
            student_users.append(user)
        
        # Get or create professors
        professors_data = [
            {"email": "professor@example.com", "first_name": "John", "last_name": "Professor", "cni": "PR001", "specialty": "Machine Learning"},
            {"email": "prof.smith@example.com", "first_name": "Emily", "last_name": "Smith", "cni": "PR002", "specialty": "Distributed Systems"},
            {"email": "prof.jones@example.com", "first_name": "Michael", "last_name": "Jones", "cni": "PR003", "specialty": "Cloud Computing"},
        ]
        
        professor_users = []
        for p_data in professors_data:
            user = db.query(User).filter(User.email == p_data["email"]).first()
            if not user:
                user = User(
                    cni=p_data["cni"],
                    last_name=p_data["last_name"],
                    first_name=p_data["first_name"],
                    email=p_data["email"],
                    hashed_password=get_password_hash("password"),
                    role=UserRole.professor
                )
                db.add(user)
                db.flush()
                print(f"✅ Created user: {user.email}")
            
            # Check if Professor record exists
            professor = db.query(Professor).filter(Professor.user_id == user.id).first()
            if not professor:
                professor = Professor(
                    user_id=user.id,
                    specialty=p_data["specialty"]
                )
                db.add(professor)
                print(f"✅ Created professor record for: {user.email}")
            
            professor_users.append(user)
        
        db.flush()
        
        # Create reports and thesis defenses
        print("\n📝 Creating thesis defenses...")
        
        defenses_data = [
            {
                "student": student_users[0],
                "title": "AI-Powered Cloud Infrastructure",
                "description": "Implementation of AI algorithms for cloud resource optimization",
                "status": "scheduled",
                "defense_date": date.today() + timedelta(days=7),
                "defense_time": time(10, 0, 0),
                "domain": "AI"
            },
            {
                "student": student_users[1],
                "title": "Big Data Analytics Platform",
                "description": "Scalable platform for real-time data processing",
                "status": "pending",
                "defense_date": None,
                "defense_time": None,
                "domain": "Data Science"
            },
            {
                "student": student_users[2],
                "title": "Deep Learning for Image Recognition",
                "description": "CNN-based system for medical image analysis",
                "status": "accepted",
                "defense_date": date.today() + timedelta(days=14),
                "defense_time": time(14, 0, 0),
                "domain": "AI"
            },
            {
                "student": student_users[3],
                "title": "Blockchain Security Framework",
                "description": "Novel approach to blockchain transaction security",
                "status": "declined",
                "defense_date": None,
                "defense_time": None,
                "domain": "Security"
            },
        ]
        
        for i, def_data in enumerate(defenses_data):
            # Create report
            report = Report(
                file_name=f"report_{i+1}.pdf",
                ai_summary=f"AI Summary: {def_data['description']}",
                ai_domain=def_data['domain'],
                ai_similarity_score=0.05 + (i * 0.03),
                student_id=def_data['student'].id
            )
            db.add(report)
            db.flush()
            
            # Create thesis defense
            defense = ThesisDefense(
                student_id=def_data['student'].id,
                title=def_data['title'],
                description=def_data['description'],
                status=def_data['status'],
                defense_date=def_data['defense_date'],
                defense_time=def_data['defense_time'],
                report_id=report.id
            )
            db.add(defense)
            db.flush()
            
            # Add jury members for scheduled/accepted defenses
            if def_data['status'] in ['scheduled', 'accepted']:
                jury1 = JuryMember(
                    thesis_defense_id=defense.id,
                    professor_id=professor_users[0].id,
                    role=JuryRole.president
                )
                jury2 = JuryMember(
                    thesis_defense_id=defense.id,
                    professor_id=professor_users[1].id,
                    role=JuryRole.member
                )
                db.add_all([jury1, jury2])
            
            print(f"✅ Created defense: {defense.title} (Status: {defense.status})")
        
        # Create notifications
        print("\n📝 Creating notifications...")
        
        for i, prof in enumerate(professor_users[:2]):
            notif = Notification(
                user_id=prof.id,
                title="Soutenance assignée",
                message=f"Vous avez été assigné à une nouvelle soutenance",
                action_type="assignment",
                is_read=False,
                creation_date=datetime.now() - timedelta(days=i)
            )
            db.add(notif)
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ COMPREHENSIVE DATA SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Summary:")
        print(f"  - Students: {len(student_users)}")
        print(f"  - Professors: {len(professor_users)}")
        print(f"  - Thesis Defenses: {len(defenses_data)}")
        print(f"  - Reports: {len(defenses_data)}")
        print("\n🎯 Manager Dashboard should now show data!")
        print("\n💡 Login credentials (all use password 'password'):")
        print("   - Manager: manager@example.com")
        print("   - Students: student@example.com, bob.student@example.com, etc.")
        print("   - Professors: professor@example.com, prof.smith@example.com, etc.")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()


if __name__ == '__main__':
    seed_comprehensive_data()
