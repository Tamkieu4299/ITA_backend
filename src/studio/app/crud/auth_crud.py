from sqlalchemy.orm import Session

from ..crud.user_crud import read_user_by_username
from ..models.user_model import User
from ..schemas.user_schema import UserLogin

def verify_password(plain_password, hashed_password):
  # This is for checking hashed_password in the future
  return True

def authenticate_user(username: str, password: str, db: Session):
  user = read_user_by_username(username, db)
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user