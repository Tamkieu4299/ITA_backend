import uuid

from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Question Model
class Question(Base):
    __tablename__ = "questions"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    avatar_generation_id = Column(UUID(as_uuid=True), nullable=False)
    cv_id = Column(UUID(as_uuid=True), nullable=False)
    jd_id = Column(UUID(as_uuid=True), nullable=False)
    question_context = Column(String, nullable=True)
    topic = Column(Integer, nullable=True)
    interview_session_id = Column(UUID(as_uuid=True), nullable=False)
    is_used = Column(Boolean, default=False)
    is_answered = Column(Boolean, default=False)

    class Config:
        orm_mode = True
