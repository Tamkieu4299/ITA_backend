import uuid
import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Interview Session Model
class Interview_session(Base):
    __tablename__ = "interview_sessions"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    cv_id = Column(UUID(as_uuid=True), nullable=False)
    jd_id = Column(UUID(as_uuid=True), nullable=False)
    interviewer_id = Column(UUID(as_uuid=True), nullable=True)
    interviewee_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, nullable=False, default="completed")
    created_at = Column(DateTime, default = datetime.datetime.now())

    class Config:
        orm_mode = True
