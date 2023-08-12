import os
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.text_crud import (
    create_text,
    delete_text,
    get_all_texts,
    get_all_texts_by_parent_id,
    read_text,
    update_text,
)
from ..db.database import get_db
from ..models.text_model import Text
from ..schemas.text_schema import TextBaseSchema, TextResponse, TextUpdate
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
    response_model=TextResponse,
)
async def add_text(
    text_data: TextBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the text"""
    text: Text = Text(**text_data.dict())
    new_text = await create_text(text, db)
    logger.info(f"Created text with ID {new_text.id}")
    return new_text.__dict__


@router.post(
    "/create_from_paragraph",
    status_code=status.HTTP_201_CREATED,
    response_model=List[TextResponse],
)
async def add_text_from_paragraph(
    text_data: TextBaseSchema,
    db: Session = Depends(get_db),
):
    """Split the paragraph"""
    text_list = list(filter(bool, text_data.text.split("\n")))
    for text_item in text_list:
        """Create the text"""
        if text_item != "":
            next
        text: Text = Text(**{"text": text_item, "parent_id": text_data.parent_id})
        new_text = await create_text(text, db)
        logger.info(f"Created text with ID {new_text.id}")

    texts = get_all_texts_by_parent_id(text_data.parent_id, db)
    texts_dict_list = [i.__dict__ for i in texts]
    return texts_dict_list


@router.put("/update/", response_model=TextResponse)
async def update_text_by_id(text: TextUpdate, db: Session = Depends(get_db)):
    """update the text by its id"""
    text_obj = update_text(text.dict(), db)
    if text_obj is None:
        logger.info(f"Invalid text with ID: {text.id}")
        raise NotFoundException(detail=f"Invalid text with ID: {text.id}")

    logger.info(f"Update text with ID: {text_obj.id}")
    return text_obj.__dict__


@router.get("/get/{id}", response_model=TextResponse)
async def get_text_by_id(id: str, db: Session = Depends(get_db)):
    """Get the text by its id"""
    text = await read_text(id, db)

    if text is None:
        logger.info(f"Invalid text with ID: {id}")
        raise NotFoundException(detail=f"Invalid text with ID: {id}")

    logger.info(f"Get text with ID: {id}")
    return text.__dict__


@router.get("/delete/{id}", response_model=List[TextResponse])
async def delete_text_by_id(id: str, db: Session = Depends(get_db)):
    """Delete text by its id"""
    result = delete_text(id, db)
    if not result:
        logger.info(f"Invalid text with ID: {id}")
        raise NotFoundException(detail=f"Invalid text with ID: {id}")

    logger.info(f"Deleted text with ID: {id}")
    texts = get_all_texts(db)
    texts_dict_list = [i.__dict__ for i in texts]
    return texts_dict_list


@router.get("/", response_model=List[TextResponse])
async def get_texts(db: Session = Depends(get_db)):
    """Get all texts"""
    texts = get_all_texts(db)
    texts_dict_list = [i.__dict__ for i in texts]
    logger.info(f"Number of texts: {len(texts)}")
    return texts_dict_list


@router.get("/get_by_parent_id/", response_model=List[TextResponse])
async def get_texts_by_parent_id(parent_id: str, db: Session = Depends(get_db)):
    """Get all texts by parent_id"""
    texts = get_all_texts_by_parent_id(parent_id, db)
    texts_dict_list = [i.__dict__ for i in texts]
    logger.info(f"Get text with jd_id: {parent_id}")
    return texts_dict_list
