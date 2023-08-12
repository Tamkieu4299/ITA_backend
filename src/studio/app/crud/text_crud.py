from sqlalchemy.orm import Session

from ..models.text_model import Text


async def create_text(text: Text, db: Session):
    db.add(text)
    db.commit()
    db.refresh(text)
    return text


async def read_text(text_id: str, db: Session):
    text = db.query(Text).filter(Text.id == text_id).first()
    return text


def update_text(text: dict, db: Session):
    db_text = db.query(Text).filter(Text.id == text["id"]).first()
    if not db_text:
        return None
    for key, value in text.items():
        if value is not None:
            setattr(db_text, key, value)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def delete_text(text_id: str, db: Session):
    db_text = db.query(Text).filter(Text.id == text_id).first()
    if not db_text:
        return False
    db.delete(db_text)
    db.commit()
    return True


def get_all_texts(db: Session):
    texts = db.query(Text).all()
    return texts


def get_all_texts_by_parent_id(parent_id: str, db: Session):
    texts = db.query(Text).filter(Text.parent_id == parent_id).all()
    return texts
