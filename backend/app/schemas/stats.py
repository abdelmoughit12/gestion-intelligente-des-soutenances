from pydantic import BaseModel
from typing import Dict, List

class MonthlyCount(BaseModel):
    month: str # Format: YYYY-MM
    count: int

class OverallStats(BaseModel):
    total_thesis_defenses: int
    total_students: int
    total_professors: int
    thesis_defenses_by_status: Dict[str, int]
    monthly_thesis_defenses: List[MonthlyCount]
