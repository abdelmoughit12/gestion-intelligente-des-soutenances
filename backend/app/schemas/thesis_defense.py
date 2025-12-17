from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .report import Report

if TYPE_CHECKING:
    from .student import Student

# Shared properties
class ThesisDefenseBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None

# Schema for creating a defense, might just be a link to a student/report
class ThesisDefenseCreate(ThesisDefenseBase):
    student_id: int
    report_id: int | None = None

# Properties to receive via API on update
class ThesisDefenseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    defense_date: date | None = None
    defense_time: time | None = None


# Properties to return to client for a list view
class ThesisDefense(ThesisDefenseBase):
    id: int
    defense_date: date | None = None
    defense_time: time | None = None
    
    # To show nested information in the response
    student: "Student"
    report: Report | None = None

    class Config:
        from_attributes = True
