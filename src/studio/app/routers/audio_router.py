import os
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.audio_crud import (
    create_audio,
    delete_audio,
    get_all_audios,
    get_all_audios_by_user,
    read_audio,
    update_audio,
)
from ..db.database import get_db
from ..models.audio_model import Audio
from ..schemas.audio_schema import AudioBaseSchema, AudioResponse, AudioUpdate
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
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=AudioResponse,
)
async def add_audio(
    audio_data: AudioBaseSchema = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Create an audio"""
    extension = validate_file_type(file, "audio")

    # Check if not an audio
    if extension is None:
        raise InvalidFileType(detail="Your upload file must be an audio")

    # Validate user_id
    if not validate_user_id(str(audio_data.user_id), db):
        logger.info(f"Invalid user with ID: {audio_data.user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {audio_data.user_id}")

    # Add metada
    file_content = await file.read()
    size = len(file_content)
    audio: Audio = Audio(**audio_data.dict())
    audio.extension = extension
    audio.size = size
    new_audio = create_audio(audio, db)
    logger.info(f"Created audio name {new_audio.file_name} with ID {new_audio.id}")

    return new_audio.__dict__


@router.get("/get/{id}", response_model=AudioResponse)
async def get_audio_by_id(id: str, db: Session = Depends(get_db)):
    """Get the audio by its id"""
    audio = read_audio(id, db)

    if audio is None:
        logger.info(f"Invalid audio with ID: {id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {id}")

    logger.info(f"Get audio with ID: {audio.id}")
    return audio.__dict__


@router.put("/update/{id}", response_model=AudioResponse)
async def update_audio_by_id(
    id: str, audio: AudioUpdate, db: Session = Depends(get_db)
):
    """Update the audio following its id"""
    audio = update_audio(id, audio, db)
    if audio is None:
        logger.info(f"Invalid audio with ID: {id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {id}")

    logger.info(f"Updated audio with ID: {id}")
    return audio.__dict__


@router.get("/delete/{id}", response_model=List[AudioResponse])
async def delete_audio_by_id(id: str, db: Session = Depends(get_db)):
    """Delete audio by its id"""
    result = delete_audio(id, db)
    if not result:
        logger.info(f"Invalid audio with ID: {id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {id}")

    logger.info(f"Deleted audio with ID: {id}")
    audios = get_all_audios(db)
    audios_dict_list = [i.__dict__ for i in audios]
    return audios_dict_list


@router.get("/", response_model=List[AudioResponse])
async def get_audios(db: Session = Depends(get_db)):
    """Get all audios"""
    audios = get_all_audios(db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Number of audios: {len(audios)}")
    return audios_dict_list


@router.get("/get_by_user/", response_model=List[AudioResponse])
async def get_audios_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """Get an image by user id"""
    # Validate user_id
    if not validate_user_id(user_id, db):
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    audios = get_all_audios_by_user(user_id, db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Get audios with user_id: {user_id}")
    return audios_dict_list
