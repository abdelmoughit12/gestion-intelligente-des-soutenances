from pydantic import BaseModel
from .user import User

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
