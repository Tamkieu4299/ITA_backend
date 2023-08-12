from typing import Optional

from pydantic import UUID4, BaseModel


class GenerationBaseSchema(BaseModel):
    id:  Optional[UUID4] = None
    user_id: UUID4
    video_id: Optional[str] = None
    audio_id: Optional[str] = None
    image_id: Optional[str] = None
    bucket_s3: Optional[str] = None
    path_s3: Optional[str] = None
    type: str

    class Config:
        orm_mode = True


class GenerationUpdate(BaseModel):
    id: UUID4
    bucket_s3: Optional[str] = None
    path_s3: Optional[str] = None

    class Config:
        orm_mode = True


class GenerationUpdateType(BaseModel):
    id: UUID4
    user_id: UUID4
    type: Optional[str] = None

    class Config:
        orm_mode = True


class GenerationCheckTypeExist(BaseModel):
    user_id: str
    type: str

    class Config:
        orm_mode = True


class GenerationResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    video_id: Optional[str] = None
    audio_id: Optional[str] = None
    image_id: Optional[str] = None
    bucket_s3: Optional[str] = None
    path_s3: Optional[str] = None
    type: str

    class Config:
        orm_mode = True
