import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.question_crud import read_question
from ..crud.jd_crud import read_jd
from ..crud.answer_crud import (
    create_answer,
    delete_answer,
    get_all_answers,
    read_answer,
    read_answer_by_question_id,
    update_answer,
)
from ..crud.text_crud import create_text, get_all_texts_by_parent_id
from ..db.database import get_db
from ..models.generation_model import Generation
from ..models.interview_session_model import Interview_session
from ..models.answer_model import Answer
from ..models.text_model import Text
from ..schemas.answer_schema import (
    AnswerBaseSchema,
    AnswerResponse,
    AnswerUpdate,
    AnswerSelectionPipelineOutput,
    AnswerSelectionPipelineInput,
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger
from ..utils.mlp_api import (
    handle_return_mlp_avatargeneration,
    handle_send_question_generation,
    handle_send_answer_analysis,
)
from ..utils.answer_analysis_utils import createAnswerAnalysisMLInputObject

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
    response_model=AnswerResponse,
)
async def add_answer(
    answer_data: AnswerBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the answer"""
    answer: Answer = Answer(**answer_data.dict())
    new_answer = await create_answer(answer, db)
    logger.info(f"Created answer with ID {new_answer.id}")
    return new_answer.__dict__


@router.put("/update/", response_model=AnswerResponse)
async def update_answer_by_id(
    answer: AnswerUpdate, db: Session = Depends(get_db)
):
    """update the answer by its id"""
    answer_obj = update_answer(answer.dict(), db)
    if answer_obj is None:
        logger.info(f"Invalid answer with ID: {answer.id}")
        raise NotFoundException(detail=f"Invalid answer with ID: {answer.id}")

    logger.info(f"Update answer with ID: {answer_obj.id}")
    return answer_obj.__dict__


@router.get("/get/{id}", response_model=AnswerResponse)
async def get_answer_by_id(id: str, db: Session = Depends(get_db)):
    """Get the answer by its id"""
    answer = await read_answer(id, db)

    if answer is None:
        logger.info(f"Invalid answer with ID: {id}")
        raise NotFoundException(detail=f"Invalid answer with ID: {id}")

    logger.info(f"Get answer with ID: {answer.id}")
    return answer.__dict__


@router.get("/get_by_question_id/{id}", response_model=AnswerResponse)
async def get_answer_by_question_id(id: str, db: Session = Depends(get_db)):
    """Get the answer by its id"""
    answer = await read_answer_by_question_id(id, db)

    if answer is None:
        logger.info(f"Invalid answer with question_id: {id}")
        raise NotFoundException(
            detail=f"Invalid answer with question_id: {id}"
        )

    logger.info(f"Get answer with question_id: {answer.id}")
    return answer.__dict__


@router.get("/delete/{id}", response_model=List[AnswerResponse])
async def delete_answer_by_id(id: str, db: Session = Depends(get_db)):
    """Delete answer by its id"""
    result = delete_answer(id, db)
    if not result:
        logger.info(f"Invalid answer with ID: {id}")
        raise NotFoundException(detail=f"Invalid answer with ID: {id}")

    logger.info(f"Deleted answer with ID: {id}")
    answers = get_all_answers(db)
    answers_dict_list = [i.__dict__ for i in answers]
    return answers_dict_list


@router.get("/", response_model=List[AnswerResponse])
async def get_answers(db: Session = Depends(get_db)):
    """Get all answers"""
    answers = get_all_answers(db)
    answers_dict_list = [i.__dict__ for i in answers]
    logger.info(f"Number of answers: {len(answers)}")
    return answers_dict_list


@router.post(
    "/send/answer_analysis", response_model=AnswerSelectionPipelineOutput
)
async def send_mlproxy_answeranalysis(
    data: AnswerSelectionPipelineInput, db: Session = Depends(get_db)
):
    # Read answer
    input_answer = await read_answer(data.answer_id, db)

    # Read question
    input_question = await read_question(input_answer.question_id, db)

    # Create ML input
    input_data = createAnswerAnalysisMLInputObject(
        input_question, input_answer, db
    )

    # Call ML proxy
    return_ml_proxy =await handle_send_answer_analysis(input_data, db)
    return return_ml_proxy
