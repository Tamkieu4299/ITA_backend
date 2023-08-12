import os
from typing import List
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.image_crud import (
    create_image,
    delete_image,
    get_all_images,
    get_all_images_by_user,
    read_image,
    update_image,
)
from ..db.database import get_db
from ..models.image_model import Image
from ..schemas.image_schema import ImageBaseSchema, ImageResponse, ImageUpdate
from ..services.validate_data import validate_user_id
from ..utils.exception import InvalidFileType, NotFoundException
from ..utils.handle_file import validate_file_type
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
    "/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=ImageResponse,
)
async def add_image(
    image_data: ImageBaseSchema = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Create an image"""
    extension = validate_file_type(file, "image")

    # Check if not an image
    if extension is None:
        raise InvalidFileType(detail="Your upload file must be an image")

    # Validate user_id
    if not validate_user_id(str(image_data.user_id), db):
        logger.info(f"Invalid user with ID: {image_data.user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {image_data.user_id}")

    # Add metada
    file_content = await file.read()
    size = len(file_content)
    image: Image = Image(**image_data.dict())
    image.extension = extension
    image.size = size
    new_image = create_image(image, db)
    logger.info(f"Created image name {new_image.file_name} with ID {new_image.id}")

    return new_image.__dict__


@router.get("/get/{id}", response_model=ImageResponse)
async def get_image_by_id(id: str, db: Session = Depends(get_db)):
    """Get an image by Id"""
    image = read_image(id, db)

    if image is None:
        logger.info(f"Invalid image with ID: {id}")
        raise NotFoundException(detail=f"Invalid image with ID: {id}")
    logger.info(f"Get image with ID: {image.id}")
    return image.__dict__


@router.get("/get_by_user/", response_model=List[ImageResponse])
async def get_images_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """Get an image by user id"""
    # Validate user_id
    if not validate_user_id(user_id, db):
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    images = get_all_images_by_user(user_id, db)
    images_dict_list = [i.__dict__ for i in images]
    logger.info(f"Get images with user_iD: {user_id}")
    return images_dict_list


@router.put("/update/{id}", response_model=ImageResponse)
async def update_image_by_id(
    id: str, image: ImageUpdate, db: Session = Depends(get_db)
):
    """Update an image file_name by its id"""
    image = update_image(id, image, db)
    if image is None:
        logger.info(f"Invalid image with ID: {id}")
        raise NotFoundException(detail=f"Invalid image with ID: {id}")

    logger.info(f"Updated image with ID: {id}")
    return image.__dict__


@router.get("/delete/{id}", response_model=List[ImageResponse])
async def delete_image_by_id(id: str, db: Session = Depends(get_db)):
    """Delete an image by its id"""
    result = delete_image(id, db)
    if not result:
        logger.info(f"Invalid image with ID: {id}")
        raise NotFoundException(detail=f"Invalid image with ID: {id}")

    logger.info(f"Deleted image with ID: {id}")
    images = get_all_images(db)
    images_dict_list = [i.__dict__ for i in images]
    return images_dict_list


@router.get("/", response_model=List[ImageResponse])
async def get_images(db: Session = Depends(get_db)):
    """Get all images"""
    images = get_all_images(db)
    images_dict_list = [i.__dict__ for i in images]
    logger.info(f"Number of images: {len(images)}")
    return images_dict_list
