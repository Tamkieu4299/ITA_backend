import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# Text Model
class Text(Base):
    __tablename__ = "texts"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    parent_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(String, nullable=True)

    class Config:
        orm_mode = True
