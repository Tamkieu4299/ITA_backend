from typing import Optional

from pydantic import UUID4, BaseModel


class JDBaseSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class JDUpdate(BaseModel):
    id: UUID4
    title: Optional[str] = None

    class Config:
        orm_mode = True


class JDResponse(BaseModel):
    id: UUID4
    title: Optional[str] = None

    class Config:
        orm_mode = True
