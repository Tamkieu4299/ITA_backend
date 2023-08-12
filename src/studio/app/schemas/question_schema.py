from typing import Optional

from pydantic import UUID4, BaseModel


class QuestionBaseSchema(BaseModel):
    avatar_generation_id: UUID4
    cv_id: UUID4
    jd_id: UUID4
    topic: int
    question_context: str

    class Config:
        orm_mode = True


class QuestionUpdate(BaseModel):
    id: UUID4
    avatar_generation_id: Optional[UUID4] = None
    topic: Optional[int] = None
    question_context: Optional[str] = None
    is_used: Optional[bool] = None
    is_anwsered: Optional[bool] = None

    class Config:
        orm_mode = True


class QuestionResponse(BaseModel):
    id: UUID4
    avatar_generation_id: UUID4
    cv_id: UUID4
    jd_id: UUID4
    topic: Optional[int] = None
    question_context: Optional[str] = None

    class Config:
        orm_mode = True


class QuestionSelectionPipelineInput(BaseModel):
    interview_session_id: UUID4
    interviewer_id: UUID4
    question_id: str
    is_answered: bool

    class Config:
        orm_mode = True

class QuestionSelectionPipelineOutput(BaseModel):
    question_id: UUID4

    class Config:
        orm_mode = True