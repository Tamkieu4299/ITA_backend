import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from ..db.database import Base


# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    username =  Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default = "interviewee")
    position = Column(String, nullable=False, default = "")

    class Config:
        orm_mode = True
