from typing import Optional

from pydantic import UUID4, BaseModel


class UserBaseSchema(BaseModel):
    username: str
    password: str
    role: Optional[str] = None
    position: Optional[str] = None

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: UUID4
    username: str
    password: str
    role: str
    position: str

    class Config:
        orm_mode = True
