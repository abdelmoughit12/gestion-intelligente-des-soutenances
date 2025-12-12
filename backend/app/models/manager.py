from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Manager(Base):
    __tablename__ = "managers"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    # Relationship back to User
    user = relationship("User", back_populates="manager_details")

    def __repr__(self):
        return f"<Manager(user_id={self.user_id})>"
