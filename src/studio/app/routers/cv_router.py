import os
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.cv_crud import (
    create_cv,
    delete_cv,
    get_all_cvs,
    get_all_cvs_by_user,
    read_cv,
    update_cv,
)
from ..db.database import get_db
from ..models.cv_model import CV
from ..schemas.cv_schema import CVBaseSchema, CVResponse, CVUpdate
from ..schemas.mlp_questiongeneration_schema import CVExtractingContents
from ..services.validate_data import validate_user_id
from ..utils.exception import (
    InvalidDestination,
    InvalidFileType,
    NotFoundException,
)
from ..utils.handle_file import validate_file_type
from ..utils.logger import setup_logger
from ..utils.mlp_api import handle_send_cv_mlproxy
from ..utils.s3_client import upload_file

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
    response_model=CVResponse,
)
async def add_cv(
    cv_data: CVBaseSchema = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Cresate the cv"""
    extension = validate_file_type(file, "application")

    # Check if not an cv
    if extension is None:
        raise InvalidFileType(detail="Your upload file must be a PDF")

    # Validate user_id
    if not validate_user_id(str(cv_data.user_id), db):
        logger.info(f"Invalid user with ID: {cv_data.user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {cv_data.user_id}")

    # Create CV
    cv_object = {
        key: value
        for key, value in cv_data.dict().items()
        if key != "bucket_name" and key != "path"
    }
    cv: CV = CV(**cv_object)
    new_cv = await create_cv(cv, db)
    res = await upload_file(
        file.file,
        cv_data.bucket_name,
        cv_data.path,
        "application",
        cv.user_id,
        f"{new_cv.id}.{extension}",
    )
    if not res["status"]:
        raise InvalidDestination(detail=res["message"])

    logger.info(f"Created CV with ID {new_cv.id}")
    return new_cv.__dict__


@router.put("/update/", response_model=CVResponse)
async def update_cv_by_id(cv: CVUpdate, db: Session = Depends(get_db)):
    """update the cv by its id"""
    cv_obj = update_cv(cv.dict(), db)
    if cv_obj is None:
        logger.info(f"Invalid CV with ID: {cv.cv_id}")
        raise NotFoundException(detail=f"Invalid CV with ID: {cv.cv_id}")

    logger.info(f"Update CV with ID: {cv_obj.id}")
    return cv_obj.__dict__


@router.get("/get/{id}", response_model=CVResponse)
async def get_cv_by_id(id: str, db: Session = Depends(get_db)):
    """Get the cv by its id"""
    cv = await read_cv(id, db)
    if cv is None:
        logger.info(f"Invalid CV with ID: {id}")
        raise NotFoundException(detail=f"Invalid CV with ID: {id}")

    logger.info(f"Get CV with ID: {id}")
    return cv.__dict__


@router.get("/delete/{id}", response_model=List[CVResponse])
async def delete_cv_by_id(id: str, db: Session = Depends(get_db)):
    """Delete cv by its id"""
    result = delete_cv(id, db)
    if not result:
        logger.info(f"Invalid CV with ID: {id}")
        raise NotFoundException(detail=f"Invalid CV with ID: {id}")

    logger.info(f"Deleted CV with ID: {id}")
    cvs = get_all_cvs(db)
    cvs_dict_list = [i.__dict__ for i in cvs]
    return cvs_dict_list


@router.get("/", response_model=List[CVResponse])
async def get_cvs(db: Session = Depends(get_db)):
    """Get all CVs"""
    cvs = get_all_cvs(db)
    cvs_dict_list = [i.__dict__ for i in cvs]
    logger.info(f"Number of CVs: {len(cvs)}")
    return cvs_dict_list


@router.get("/get_by_user/", response_model=List[CVResponse])
async def get_cvs_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """Get all cvs by user id"""
    # Validate user_id
    if not validate_user_id(user_id, db):
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    cvs = get_all_cvs_by_user(user_id, db)
    cvs_dict_list = [i.__dict__ for i in cvs]
    logger.info(f"Get CVs with user_id: {user_id}")
    return cvs_dict_list


@router.post("/send/cv_extracting")
async def send_mlproxy_cvextracting(
    data: CVExtractingContents = Depends(), db: Session = Depends(get_db)
):
    """Send CV file to ML proxy to extract keywords and update to CV model"""
    cv = await read_cv(data.cv_id, db)
    key_file = f"{data.path}/application/{cv.user_id}/{cv.id}.pdf"
    input_data = {
        "cv_id": cv.id,
        "bucket": data.bucket_name,
        "key_file": key_file,
    }
    return_mlp = await handle_send_cv_mlproxy(input_data, db)
    return return_mlp
