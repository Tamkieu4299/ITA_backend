from typing import Optional

from pydantic import BaseModel


class MLPBaseAvatarGenerationSchema(BaseModel):
    bucket_name: str
    task_id: str
    video_key: Optional[str]
    image_key: Optional[str]
    audio_key: str
    text: Optional[str]

    class Config:
        orm_mode = True


class VideoURL(BaseModel):
    bucket: str
    key_file: str


class MLPInputAvatarGenerationSchema(BaseModel):
    task_id: str
    video_url: VideoURL

    class Config:
        orm_mode = True
