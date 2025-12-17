from pydantic import BaseModel
from .professor import Professor

from app.models.jury_member import JuryRole # Use the enum from models

# Shared properties
class JuryMemberBase(BaseModel):
    role: JuryRole # Use the Enum

# Properties to receive via API on creation
class JuryMemberCreate(JuryMemberBase):
    professor_id: int
    thesis_defense_id: int

# Properties to return to client
class JuryMember(JuryMemberBase):
    thesis_defense_id: int
    professor_id: int
    professor: Professor # Nested Professor schema
    # thesis_defense: ThesisDefense # Only nest if required, for now just show ID

    class Config:
        from_attributes = True

# Properties to receive via API on update
class JuryMemberUpdate(JuryMemberBase):
    professor_id: int | None = None
    role: JuryRole | None = None
