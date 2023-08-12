from pydantic import BaseModel


class CVExtractingContents(BaseModel):
    cv_id: str
    bucket_name: str
    path: str

    class Config:
        orm_mode = True


class QuestionGenerationContents(BaseModel):
    cv_id: str
    bucket_name: str
    path: str
    jd_id: str

    class Config:
        orm_mode = True
