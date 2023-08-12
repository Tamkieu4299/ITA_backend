import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Image Model
class Image(Base):
    __tablename__ = "images"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    file_name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False)

    class Config:
        orm_mode = True
