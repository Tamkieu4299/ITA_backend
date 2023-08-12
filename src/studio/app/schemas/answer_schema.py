from typing import Optional

from pydantic import UUID4, BaseModel


class AnswerBaseSchema(BaseModel):
    question_id: UUID4
    bucket_s3: str
    video_url: str
    audio_url: str

    class Config:
        orm_mode = True


class AnswerUpdate(BaseModel):
    id: UUID4
    bucket_s3: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    overall_score: Optional[float] = None
    confidence_score: Optional[float] = None
    text_relevancy_score: Optional[float] = None
    has_bad_words: Optional[bool] = None
    professional_score: Optional[float] = None
    emotion_from_text: Optional[str] = None
    emotion_from_audio: Optional[str] = None
    emotion_from_video: Optional[str] = None

    class Config:
        orm_mode = True


class AnswerResponse(BaseModel):
    id: UUID4
    question_id: UUID4
    bucket_s3: str
    video_url: str
    audio_url: str
    overall_score: Optional[float] = None
    confidence_score: Optional[float] = None
    text_relevancy_score: Optional[float] = None
    has_bad_words: Optional[bool] = None
    professional_score: Optional[float] = None
    emotion_from_text: Optional[str] = None
    emotion_from_audio: Optional[str] = None
    emotion_from_video: Optional[str] = None

    class Config:
        orm_mode = True


class AnswerSelectionPipelineInput(BaseModel):
    answer_id: UUID4


class AnswerSelectionPipelineOutput(BaseModel):
    task_id: UUID4
    overall_score: Optional[float] = None
    confidence_score: Optional[float] = None
    text_relevancy_score: Optional[float] = None
    has_bad_words: Optional[bool] = None
    professional_score: Optional[float] = None
    emotion_from_text: Optional[str] = None
    emotion_from_audio: Optional[str] = None
    emotion_from_video: Optional[str] = None

    class Config:
        orm_mode = True
