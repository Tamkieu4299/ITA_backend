from typing import Optional
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import UserBaseSchema


def create_user(user: User, db: Session):
    if db.query(User).filter(User.username == user.username).first():
        pass

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user(user_id: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    return user

def read_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user


def delete_user(user_id: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


def get_users(db: Session, role: Optional[str] = None):
    users = db.query(User).filter(User.role == role if role is not None else True).all()
    return users
