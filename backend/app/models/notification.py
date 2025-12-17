from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    title = Column(String(500), nullable=True) # "Titre"
    message = Column(Text, nullable=True) # "Message"
    action_type = Column(String(250), nullable=True) # "Type_Action"
    creation_date = Column(DateTime, server_default=func.now()) # "Date_creation"
    is_read = Column(Boolean, default=False) # "Est_Lue"

    # Relationship back to User
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id})>"
