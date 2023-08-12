from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models.interview_session_model import Interview_session


async def create_interview_session(interview_session: Interview_session, db: Session):
    db.add(interview_session)
    db.commit()
    db.refresh(interview_session)
    return interview_session


async def read_interview_session(interview_session_id: str, db: Session):
    interview_session = (
        db.query(Interview_session)
        .filter(Interview_session.id == interview_session_id)
        .first()
    )
    return interview_session


def update_interview_session(interview_session: dict, db: Session):
    db_interview_session = (
        db.query(Interview_session)
        .filter(Interview_session.id == interview_session["id"])
        .first()
    )
    if not db_interview_session:
        return None
    for key, value in interview_session.items():
        if value is not None:
            setattr(db_interview_session, key, value)
    db.add(db_interview_session)
    db.commit()
    db.refresh(db_interview_session)
    return db_interview_session


def delete_interview_session(interview_session_id: str, db: Session):
    db_interview_session = (
        db.query(Interview_session)
        .filter(Interview_session.id == interview_session_id)
        .first()
    )
    if not db_interview_session:
        return False
    db.delete(db_interview_session)
    db.commit()
    return True


def get_all_interview_sessions(db: Session):
    interview_sessions = db.query(Interview_session).all()
    return interview_sessions


def get_all_interview_sessions_by_cv_and_jd(cv_id: str, jd_id: str, db: Session):
    interview_sessions = (
        db.query(Interview_session)
        .filter(
            and_(
                Interview_session.cv_id == cv_id,
                Interview_session.jd_id == jd_id,
            )
        )
        .all()
    )
    return interview_sessions
