import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Generation Model
class Generation(Base):
    __tablename__ = "generations"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    video_id = Column(String, nullable=True)
    audio_id = Column(String, nullable=True)
    image_id = Column(String, nullable=True)
    bucket_s3 = Column(String, nullable=True)
    path_s3 = Column(String, nullable=True)
    type = Column(String, nullable=False, default="generated")

    class Config:
        orm_mode = True
