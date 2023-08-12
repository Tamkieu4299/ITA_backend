import os
from typing import List
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.video_crud import (
    create_video,
    delete_video,
    get_all_videos,
    get_all_videos_by_user,
    read_video,
    update_video,
)
from ..db.database import get_db
from ..models.video_model import Video
from ..schemas.video_schema import VideoBaseSchema, VideoResponse, VideoUpdate
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
    response_model=VideoResponse,
)
async def add_video(
    video_data: VideoBaseSchema = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Create an video"""
    extension = validate_file_type(file, "video")

    # Check if not an video
    if extension is None:
        raise InvalidFileType(detail="Your upload file must be a video")

    # Validate user_id
    if not validate_user_id(str(video_data.user_id), db):
        logger.info(f"Invalid user with ID: {video_data.user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {video_data.user_id}")

    # Add metada
    file_content = await file.read()
    size = len(file_content)
    video: Video = Video(**video_data.dict())
    video.extension = extension
    video.size = size
    new_video = create_video(video, db)
    logger.info(f"Created video name {new_video.file_name} with ID {new_video.id}")

    return new_video.__dict__


@router.get("/get/{id}", response_model=VideoResponse)
async def get_video_by_id(id: str, db: Session = Depends(get_db)):
    """Get the video by its id"""
    video = read_video(id, db)

    if video is None:
        logger.info(f"Invalid video with ID: {id}")
        raise NotFoundException(detail=f"Invalid video with ID: {id}")

    logger.info(f"Get video with ID: {video.id}")
    return video.__dict__


@router.put("/update/{id}", response_model=VideoResponse)
async def update_video_by_id(
    id: str, video: VideoUpdate, db: Session = Depends(get_db)
):
    """Update the video following its id"""
    video = update_video(id, video, db)
    if video is None:
        logger.info(f"Invalid video with ID: {id}")
        raise NotFoundException(detail=f"Invalid video with ID: {id}")

    logger.info(f"Updated video with ID: {id}")
    return video.__dict__


@router.get("/delete/{id}", response_model=List[VideoResponse])
async def delete_video_by_id(id: str, db: Session = Depends(get_db)):
    """Delete video by its id"""
    result = delete_video(id, db)
    if not result:
        logger.info(f"Invalid video with ID: {id}")
        raise NotFoundException(detail=f"Invalid video with ID: {id}")

    logger.info(f"Deleted video with ID: {id}")
    videos = get_all_videos(db)
    videos_dict_list = [i.__dict__ for i in videos]
    return videos_dict_list


@router.get("/", response_model=List[VideoResponse])
async def get_videos(db: Session = Depends(get_db)):
    """Get all videos"""
    videos = get_all_videos(db)
    videos_dict_list = [i.__dict__ for i in videos]
    logger.info(f"Number of videos: {len(videos)}")
    return videos_dict_list


@router.get("/get_by_user/", response_model=List[VideoResponse])
async def get_videos_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """Get an image by user id"""
    # Validate user_id
    if not validate_user_id(user_id, db):
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    videos = get_all_videos_by_user(user_id, db)
    videos_dict_list = [i.__dict__ for i in videos]
    logger.info(f"Get videos with user_id: {user_id}")
    return videos_dict_list
