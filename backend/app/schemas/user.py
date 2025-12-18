from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    cni: Optional[str] = None
    role: UserRole # Ensure role is of type UserRole enum

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to client
class User(UserBase):
    id: int

    class Config:
        from_attributes = True # for Pydantic v2

# Properties stored in DB
class UserInDB(User):
    hashed_password: str
