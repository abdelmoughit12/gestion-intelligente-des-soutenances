from __future__ import annotations

from datetime import date, time
from typing import List

from pydantic import BaseModel

from .student import Student
from .report import Report
from .jury_member import JuryMember


# Shared properties
class ThesisDefenseBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None


# Schema for creating a defense
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


# Properties to return to client
class ThesisDefense(ThesisDefenseBase):
    id: int
    defense_date: date | None = None
    defense_time: time | None = None

    student: Student
    report: Report | None = None
    jury_members: List[JuryMember] = []

    class Config:
        from_attributes = True
