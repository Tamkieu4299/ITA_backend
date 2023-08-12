import uuid
from typing import List

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# JD Model
class JD(Base):
    __tablename__ = "jds"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    title = Column(String, nullable=True)

    class Config:
        orm_mode = True
