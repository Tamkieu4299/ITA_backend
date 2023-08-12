import os
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.jd_crud import (
    create_jd,
    delete_jd,
    get_all_jds,
    get_all_jds_by_title,
    read_jd,
    update_jd,
)
from ..db.database import get_db
from ..models.jd_model import JD
from ..schemas.jd_schema import JDBaseSchema, JDResponse, JDUpdate
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()
# Serve static files
router.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        + "/static"
    ),
    name="static",
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=JDResponse,
)
async def add_jd(
    jd_data: JDBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the jd"""
    jd: JD = JD(**jd_data.dict())
    new_jd = await create_jd(jd, db)
    logger.info(f"Created jd with ID {new_jd.id}")
    return new_jd.__dict__


@router.put("/update/", response_model=JDResponse)
async def update_jd_by_id(jd: JDUpdate, db: Session = Depends(get_db)):
    """update the jd by its id"""
    jd_obj = update_jd(jd.dict(), db)
    if jd_obj is None:
        logger.info(f"Invalid JD with ID: {jd.id}")
        raise NotFoundException(detail=f"Invalid JD with ID: {jd.id}")

    logger.info(f"Update JD with ID: {jd_obj.id}")
    return jd_obj.__dict__


@router.get("/get/{id}", response_model=JDResponse)
async def get_jd_by_id(id: str, db: Session = Depends(get_db)):
    """Get the jd by its id"""
    jd = await read_jd(id, db)

    if jd is None:
        logger.info(f"Invalid jd with ID: {id}")
        raise NotFoundException(detail=f"Invalid JD with ID: {id}")

    logger.info(f"Get JD with ID: {id}")
    return jd.__dict__


@router.get("/delete/{id}", response_model=List[JDResponse])
async def delete_jd_by_id(id: str, db: Session = Depends(get_db)):
    """Delete jd by its id"""
    result = delete_jd(id, db)
    if not result:
        logger.info(f"Invalid JD with ID: {id}")
        raise NotFoundException(detail=f"Invalid JD with ID: {id}")

    logger.info(f"Deleted jd with ID: {id}")
    jds = get_all_jds(db)
    jds_dict_list = [i.__dict__ for i in jds]
    return jds_dict_list


@router.get("/", response_model=List[JDResponse])
async def get_jds(db: Session = Depends(get_db)):
    """Get all jds"""
    jds = get_all_jds(db)
    jds_dict_list = [i.__dict__ for i in jds]
    logger.info(f"Number of JDs: {len(jds)}")
    return jds_dict_list


@router.get("/get_by_title/", response_model=List[JDResponse])
async def get_jds_by_title(title: str, db: Session = Depends(get_db)):
    """Get all jds by title"""
    jds = get_all_jds_by_title(title, db)
    jds_dict_list = [i.__dict__ for i in jds]
    logger.info(f"Get JD with title: {title}")
    return jds_dict_list
