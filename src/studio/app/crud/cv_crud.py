from sqlalchemy.orm import Session

from ..models.cv_model import CV


async def create_cv(cv: CV, db: Session):
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


async def read_cv(cv_id: str, db: Session):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    return cv


def update_cv(cv: dict, db: Session):
    db_cv = db.query(CV).filter(CV.id == cv["cv_id"]).first()
    if not db_cv:
        return None
    for key, value in cv.items():
        if value is not None:
            setattr(db_cv, key, value)
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    return db_cv


def delete_cv(cv_id: str, db: Session):
    db_cv = db.query(CV).filter(CV.id == cv_id).first()
    if not db_cv:
        return False
    db.delete(db_cv)
    db.commit()
    return True


def get_all_cvs(db: Session):
    cvs = db.query(CV).all()
    return cvs


def get_all_cvs_by_user(user_id: str, db: Session):
    cvs = db.query(CV).filter(CV.user_id == user_id).all()
    return cvs
