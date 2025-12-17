from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base
import enum

class ReportAction(str, enum.Enum):
    view = "view"
    download = "download"
    recover = "recover"

class ReportAccess(Base):
    __tablename__ = "report_access_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    action = Column(SQLAlchemyEnum(ReportAction), nullable=False)
    action_date = Column(DateTime, server_default=func.now()) # "date_action"
    comment = Column(String(500), nullable=True) # "commentaire"

    # Relationships
    report = relationship("Report", backref="access_logs")
    professor = relationship("Professor", backref="report_access_actions")

    def __repr__(self):
        return f"<ReportAccess(id={self.id}, report_id={self.report_id}, professor_id={self.professor_id})>"
