from pydantic import BaseModel
from .user import User

# Shared properties
class ProfessorBase(BaseModel):
    specialty: str | None = None

# Properties to receive via API on creation (if we were to create Professor directly)
class ProfessorCreate(ProfessorBase):
    user_id: int # To link to an existing user

# Properties to return to client
class Professor(ProfessorBase):
    user_id: int
    user: User # Nested User schema

    class Config:
        from_attributes = True
