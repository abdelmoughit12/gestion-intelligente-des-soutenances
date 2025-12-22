from pydantic import BaseModel, EmailStr
from .user import User

# Shared properties
class ProfessorBase(BaseModel):
    specialty: str | None = None

# Schema for creating a new professor record including user details
class ProfessorCreateData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    specialty: str

# Properties to receive via API on creation (if we were to create Professor directly)
class ProfessorCreate(ProfessorBase):
    user_id: int # To link to an existing user

# Properties to return to client
class Professor(ProfessorBase):
    user_id: int
    user: User # Nested User schema

    class Config:
        from_attributes = True
