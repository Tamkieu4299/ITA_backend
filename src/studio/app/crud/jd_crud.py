from sqlalchemy.orm import Session

from ..models.jd_model import JD


async def create_jd(jd: JD, db: Session):
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


async def read_jd(jd_id: str, db: Session):
    jd = db.query(JD).filter(JD.id == jd_id).first()
    return jd


def update_jd(jd: dict, db: Session):
    db_jd = db.query(JD).filter(JD.id == jd["id"]).first()
    if not db_jd:
        return None
    for key, value in jd.items():
        if value is not None:
            setattr(db_jd, key, value)
    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)
    return db_jd


def delete_jd(jd_id: str, db: Session):
    db_jd = db.query(JD).filter(JD.id == jd_id).first()
    if not db_jd:
        return False
    db.delete(db_jd)
    db.commit()
    return True


def get_all_jds(db: Session):
    jds = db.query(JD).all()
    return jds


def get_all_jds_by_title(title: str, db: Session):
    jds = db.query(JD).filter(JD.title == title).all()
    return jds
