import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.interview_session_crud import (
    create_interview_session,
    delete_interview_session,
    get_all_interview_sessions,
    get_all_interview_sessions_by_cv_and_jd,
    read_interview_session,
)
from ..db.database import get_db
from ..models.interview_session_model import Interview_session
from ..schemas.interview_session_schema import (
    Interview_sessionBaseSchema,
    Interview_sessionResponse,
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()
# Serve static files
router.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        + "/static"
    ),
    name="static",
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=Interview_sessionResponse,
)
async def add_interview_session(
    interview_session_data: Interview_sessionBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the interview_session"""
    interview_session: Interview_session = Interview_session(
        **interview_session_data.dict()
    )
    new_interview_session = await create_interview_session(
        interview_session, db
    )
    logger.info(
        f"Created interview_session with ID {new_interview_session.id}"
    )
    return new_interview_session.__dict__


@router.get("/get/{id}", response_model=Interview_sessionResponse)
async def get_interview_session_by_id(id: str, db: Session = Depends(get_db)):
    """Get the interview_session by its id"""
    interview_session = await read_interview_session(id, db)

    if interview_session is None:
        logger.info(f"Invalid interview_session with ID: {id}")
        raise NotFoundException(
            detail=f"Invalid interview_session with ID: {id}"
        )

    logger.info(f"Get interview_session with ID: {interview_session.id}")
    return interview_session.__dict__


@router.get("/delete/{id}", response_model=List[Interview_sessionResponse])
async def delete_interview_session_by_id(
    id: str, db: Session = Depends(get_db)
):
    """Delete interview_session by its id"""
    result = delete_interview_session(id, db)
    if not result:
        logger.info(f"Invalid interview_session with ID: {id}")
        raise NotFoundException(
            detail=f"Invalid interview_session with ID: {id}"
        )

    logger.info(f"Deleted interview_session with ID: {id}")
    interview_sessions = get_all_interview_sessions(db)
    interview_sessions_dict_list = [i.__dict__ for i in interview_sessions]
    return interview_sessions_dict_list


@router.get("/", response_model=List[Interview_sessionResponse])
async def get_interview_sessions(db: Session = Depends(get_db)):
    """Get all interview_sessions"""
    interview_sessions = get_all_interview_sessions(db)
    interview_sessions_dict_list = [i.__dict__ for i in interview_sessions]
    logger.info(f"Number of interview_sessions: {len(interview_sessions)}")
    return interview_sessions_dict_list


@router.get(
    "/get_by_cv_and_jd/", response_model=List[Interview_sessionResponse]
)
async def get_interview_sessions_by_cv_and_jd(
    cv_id: str, jd_id: str, db: Session = Depends(get_db)
):
    """Get all interview_sessions by user id"""
    interview_sessions = get_all_interview_sessions_by_cv_and_jd(
        cv_id, jd_id, db
    )
    interview_sessions_dict_list = [i.__dict__ for i in interview_sessions]
    logger.info(f"Get interview_sessions with cv_id {cv_id} and jd_id {jd_id}")
    return interview_sessions_dict_list
