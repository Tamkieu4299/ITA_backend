from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class CVBaseSchema(BaseModel):
    user_id: UUID4
    full_name: str
    email: EmailStr
    phone_number: str
    description: str
    optional_infor: Optional[str] = None
    bucket_name: str
    path: str

    class Config:
        orm_mode = True


class CVUpdate(BaseModel):
    cv_id: UUID4
    optional_infor: Optional[str] = None
    texts: Optional[str] = None

    class Config:
        orm_mode = True


class CVResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    full_name: str
    email: EmailStr
    phone_number: str
    description: str
    optional_infor: Optional[str] = None
    texts: Optional[str] = None

    class Config:
        orm_mode = True
