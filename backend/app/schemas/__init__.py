from .user import User, UserCreate
from .student import Student, StudentCreate
from .student import StudentDashboardStats
from .report import Report, ReportCreate, ReportUpdate
from .thesis_defense import ThesisDefense, ThesisDefenseCreate, ThesisDefenseUpdate
from .professor import Professor, ProfessorCreate
from .jury_member import JuryMember, JuryMemberCreate, JuryMemberUpdate

# Resolve forward references (Pydantic v2) for schemas that refer to each other.
Student.model_rebuild(force=True)
ThesisDefense.model_rebuild(force=True)
StudentDashboardStats.model_rebuild(force=True)
