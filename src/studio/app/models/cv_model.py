import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON, UUID

from ..db.database import Base


# CV Model
class CV(Base):
    __tablename__ = "cvs"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    description = Column(String, nullable=False)
    optional_infor = Column(JSON, nullable=True)

    class Config:
        orm_mode = True
