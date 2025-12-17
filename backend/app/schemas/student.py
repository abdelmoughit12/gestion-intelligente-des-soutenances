from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .user import User

if TYPE_CHECKING:
    from .thesis_defense import ThesisDefense

# Shared properties
class StudentBase(BaseModel):
    major: str | None = None
    cne: str | None = None
    year: int | None = None

# Properties to receive via API on creation
class StudentCreate(StudentBase):
    pass # Add any specific fields for student creation

# Properties to return to client
class Student(StudentBase):
    user: User # This will nest the User schema in the response

    class Config:
        from_attributes = True


class StudentDashboardStats(BaseModel):
    total: int
    pending: int
    accepted: int
    refused: int
    recent_requests: list["ThesisDefense"] = []
    upcoming_defenses: list["ThesisDefense"] = []

    class Config:
        from_attributes = True
