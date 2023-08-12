import uuid

from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Answer Model
class Answer(Base):
    __tablename__ = "answers"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    question_id = Column(UUID(as_uuid=True), nullable=False)
    bucket_s3 = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    audio_url = Column(String, nullable=False)
    overall_score = Column(Float, nullable=False, default=0.0)
    confidence_score = Column(Float, nullable=False, default=0.0)
    text_relevancy_score = Column(Float, nullable=False, default=0.0)
    has_bad_words = Column(Boolean, nullable=False, default=False)
    professional_score = Column(Float, nullable=False, default=0.0)
    emotion_from_text = Column(String, nullable=False, default="")
    emotion_from_audio = Column(String, nullable=False, default="")
    emotion_from_video = Column(String, nullable=False, default="")

    class Config:
        orm_mode = True
