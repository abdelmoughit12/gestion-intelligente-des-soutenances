from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from collections import defaultdict
from ..models import ThesisDefense, Student, Professor

def get_overall_stats(db: Session):
    # Total counts
    total_thesis_defenses = db.query(ThesisDefense).count()
    total_students = db.query(Student).count()
    total_professors = db.query(Professor).count()

    # Thesis defenses by status
    defenses_by_status_query = db.query(ThesisDefense.status, func.count(ThesisDefense.id))\
                                .group_by(ThesisDefense.status).all()
    thesis_defenses_by_status = {status: count for status, count in defenses_by_status_query if status is not None}

    # Monthly thesis defenses
    # Filter out defenses without a defense_date
    monthly_defenses_query = db.query(
        func.to_char(ThesisDefense.defense_date, 'YYYY-MM').label('month'),
        func.count(ThesisDefense.id)
    ).filter(ThesisDefense.defense_date.isnot(None))\
     .group_by('month')\
     .order_by('month')\
     .all()
    
    monthly_thesis_defenses = [{"month": month, "count": count} for month, count in monthly_defenses_query]

    return {
        "total_thesis_defenses": total_thesis_defenses,
        "total_students": total_students,
        "total_professors": total_professors,
        "thesis_defenses_by_status": thesis_defenses_by_status,
        "monthly_thesis_defenses": monthly_thesis_defenses,
    }

