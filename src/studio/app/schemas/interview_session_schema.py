import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

class Interview_sessionBaseSchema(BaseModel):
    id: UUID4
    cv_id: UUID4
    jd_id: UUID4
    interviewer_id: Optional[UUID4]
    interviewee_id: Optional[UUID4]
    created_at: datetime.datetime = datetime.datetime.now()
    status: Optional[str]

    class Config:
        orm_mode = True


class Interview_sessionResponse(BaseModel):
    id: UUID4
    cv_id: UUID4
    jd_id: UUID4
    interviewer_id: Optional[UUID4]
    interviewee_id: Optional[UUID4]
    created_at: datetime.datetime = datetime.datetime.now()
    status: Optional[str]


    class Config:
        orm_mode = True
