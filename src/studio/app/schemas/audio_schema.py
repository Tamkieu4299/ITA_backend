from typing import Optional

from pydantic import UUID4, BaseModel


class AudioBaseSchema(BaseModel):
    user_id: UUID4
    file_name: str
    language: str
    duration: int

    class Config:
        orm_mode = True


class AudioUpdate(BaseModel):
    file_name: Optional[str]

    class Config:
        orm_mode = True


class AudioResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    file_name: str
    language: str
    extension: str
    size: int
    duration: int

    class Config:
        orm_mode = True
