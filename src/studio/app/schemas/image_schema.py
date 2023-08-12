from typing import Optional

from pydantic import UUID4, BaseModel


class ImageBaseSchema(BaseModel):
    user_id: UUID4
    file_name: str

    class Config:
        orm_mode = True


class ImageUpdate(BaseModel):
    file_name: Optional[str]

    class Config:
        orm_mode = True


class ImageResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    file_name: str
    extension: str
    size: int

    class Config:
        orm_mode = True
