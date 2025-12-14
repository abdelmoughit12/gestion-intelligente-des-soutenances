from pydantic import BaseModel
from datetime import datetime

# Shared properties
class ReportBase(BaseModel):
    file_name: str
    ai_summary: str | None = None
    ai_domain: str | None = None
    ai_similarity_score: float | None = None

# Properties to receive via API on creation
class ReportCreate(ReportBase):
    student_id: int

# Properties to receive via API on update
class ReportUpdate(BaseModel):
    file_name: str | None = None
    ai_summary: str | None = None
    ai_domain: str | None = None
    ai_similarity_score: float | None = None

# Properties to return to client
class Report(ReportBase):
    id: int
    student_id: int | None = None
    submission_date: datetime

    class Config:
        from_attributes = True
