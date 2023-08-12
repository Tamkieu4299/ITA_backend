from typing import Optional

from pydantic import UUID4, BaseModel


class TextBaseSchema(BaseModel):
    text: str
    parent_id: UUID4

    class Config:
        orm_mode = True


class TextUpdate(BaseModel):
    id: UUID4
    text: Optional[str] = None

    class Config:
        orm_mode = True


class TextResponse(BaseModel):
    id: UUID4
    text: str
    parent_id: UUID4

    class Config:
        orm_mode = True
