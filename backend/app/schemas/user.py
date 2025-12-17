from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    role: str # In a real app, this might be set automatically
    cni: str | None = None

# Properties to return to client
class User(UserBase):
    id: int
    cni: str | None = None
    role: str

    class Config:
        from_attributes = True # for Pydantic v2
