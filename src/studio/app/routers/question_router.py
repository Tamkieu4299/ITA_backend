import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.cv_crud import read_cv
from ..crud.generation_crud import create_generation, get_all_base_generations
from ..crud.interview_session_crud import (
    create_interview_session,
)
from ..crud.jd_crud import read_jd
from ..crud.question_crud import (
    create_question,
    delete_question,
    get_all_questions,
    get_all_questions_by_interview_session_id,
    get_all_questions_by_interviewer_id_and_interview_session_id,
    read_question,
    update_question,
)
from ..crud.text_crud import create_text, get_all_texts_by_parent_id
from ..db.database import get_db
from ..models.generation_model import Generation
from ..models.interview_session_model import Interview_session
from ..models.question_model import Question
from ..models.text_model import Text
from ..schemas.mlp_questiongeneration_schema import QuestionGenerationContents
from ..schemas.question_schema import (
    QuestionBaseSchema,
    QuestionResponse,
    QuestionUpdate,
    QuestionSelectionPipelineInput,
    QuestionSelectionPipelineOutput,
)
from ..utils.exception import NotFoundException
from ..utils.logger import setup_logger
from ..utils.mlp_api import (
    handle_return_mlp_avatargeneration,
    handle_send_question_generation,
    handle_send_question_selection,
)
from ..utils.question_selection_utils import (
    createQuestionObjectDict,
    createAskedQuestionObjectDict,
    createQuestionBankDict,
    createMLInput,
)

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
    response_model=QuestionResponse,
)
async def add_question(
    question_data: QuestionBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the question"""
    question: Question = Question(**question_data.dict())
    new_question = await create_question(question, db)
    logger.info(f"Created question with ID {new_question.id}")
    return new_question.__dict__


@router.put("/update/", response_model=QuestionResponse)
async def update_question_by_id(
    question: QuestionUpdate, db: Session = Depends(get_db)
):
    """update the question by its id"""
    question_obj = update_question(question.dict(), db)
    if question_obj is None:
        logger.info(f"Invalid question with ID: {question.id}")
        raise NotFoundException(
            detail=f"Invalid question with ID: {question.id}"
        )

    logger.info(f"Update question with ID: {question_obj.id}")
    return question_obj.__dict__


@router.get("/get/{id}", response_model=QuestionResponse)
async def get_question_by_id(id: str, db: Session = Depends(get_db)):
    """Get the question by its id"""
    question = await read_question(id, db)

    if question is None:
        logger.info(f"Invalid question with ID: {id}")
        raise NotFoundException(detail=f"Invalid question with ID: {id}")

    logger.info(f"Get question with ID: {question.id}")
    return question.__dict__


@router.get("/delete/{id}", response_model=List[QuestionResponse])
async def delete_question_by_id(id: str, db: Session = Depends(get_db)):
    """Delete question by its id"""
    result = delete_question(id, db)
    if not result:
        logger.info(f"Invalid question with ID: {id}")
        raise NotFoundException(detail=f"Invalid question with ID: {id}")

    logger.info(f"Deleted question with ID: {id}")
    questions = get_all_questions(db)
    questions_dict_list = [i.__dict__ for i in questions]
    return questions_dict_list


@router.get("/", response_model=List[QuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    """Get all questions"""
    questions = get_all_questions(db)
    questions_dict_list = [i.__dict__ for i in questions]
    logger.info(f"Number of questions: {len(questions)}")
    return questions_dict_list


@router.get(
    "/get_by_interview_session/", response_model=List[QuestionResponse]
)
async def get_questions_by_interview_session(
    interview_session_id: str, db: Session = Depends(get_db)
):
    """Get all questions by interview session id"""
    questions = get_all_questions_by_interview_session_id(
        interview_session_id, db
    )
    questions_dict_list = [i.__dict__ for i in questions]
    logger.info(
        f"Get questions with interview_session_id {interview_session_id}"
    )
    return questions_dict_list


@router.post("/send/question_generation")
async def send_mlproxy_questiongeneration(
    data: QuestionGenerationContents = Depends(), db: Session = Depends(get_db)
):
    """Send message to ML proxy to generate questions"""
    # Get the id of CV
    get_cv = await read_cv(data.cv_id, db)
    if not get_cv:
        logger.info(f"Invalid cv with ID: {data.cv_id}")
        raise NotFoundException(detail=f"Invalid cv with ID: {data.cv_id}")

    # get the texts of JD
    get_jd = await read_jd(data.jd_id, db)

    # Create interview sessio Object
    new_interview_session_data = {
        "cv_id": data.cv_id,
        "jd_id": data.jd_id,
    }
    new_interview_session_obj: Interview_session = Interview_session(
        **new_interview_session_data
    )
    interview_session = await create_interview_session(
        new_interview_session_obj, db
    )

    if not get_jd:
        logger.info(f"Invalid jd with ID: {data.jd_id}")
        raise NotFoundException(detail=f"Invalid jd with ID: {data.jd_id}")

    # get the list of texts following jd_id
    jd_texts = get_all_texts_by_parent_id(data.jd_id, db)
    texts = [jd_text.text for jd_text in jd_texts]

    # Get the list of questions from ML
    input_data_question_generation = {
        "task_id": interview_session.id,
        "cv_url": {
            "bucket": data.bucket_name,
            "key_file": f"{data.path}/application/{get_cv.user_id}/{data.cv_id}.pdf",
        },
        "jd_texts": texts,
    }
    response_data = await handle_send_question_generation(
        input_data_question_generation
    )

    questions = response_data["questions"]
    cv_texts = response_data["cv_texts"]

    # Get all generation base videos (Base videos mean all generated videos will depends on those)
    base_avatar_generations = await get_all_base_generations(db)

    base_avatar_generations_list = [
        {k: v for k, v in gen.__dict__.items() if not k.startswith("_")}
        for gen in base_avatar_generations
    ]

    # Loop thourgh base avatar generation videos
    for generation_base in base_avatar_generations_list:
        generation_data = generation_base
        generation_data["type"] = "generated"

        # Loop through questions and create generation schema
        for question in questions:
            uuid_value = uuid.uuid4()
            generation_data["id"] = uuid_value
            generation_object: Generation = Generation(**generation_data)
            new_generation_question = await create_generation(
                generation_object, db, generation_data
            )
            # Generate avatar based on question
            input_data = {"task_id": uuid_value}
            if generation_object.video_id:
                video_url = {}
                video_url["bucket"] = new_generation_question.bucket_s3
                video_url[
                    "key_file"
                ] = f"server-test-01/video/${new_generation_question.user_id}/${new_generation_question.video_id}.mp4"
                input_data["video_url"] = video_url

            if generation_object.audio_id:
                audio_url = {}
                audio_url["bucket"] = new_generation_question.bucket_s3
                audio_url[
                    "key_file"
                ] = f"server-test-01/audio/${new_generation_question.user_id}/${new_generation_question.audio_id}.wav"
                input_data["audio_url"] = audio_url

            if generation_object.image_id:
                image_url = {}
                image_url["bucket"] = new_generation_question.bucket_s3
                image_url[
                    "key_file"
                ] = f"server-test-01/image/${new_generation_question.user_id}/${new_generation_question.image_id}.jpg"
                input_data["image_url"] = image_url

            input_data["text"] = question["question"]
            return_mlp = await handle_return_mlp_avatargeneration(
                input_data, input_data, db
            )

            # Add question into db
            new_question_data = {
                "avatar_generation_id": return_mlp["id"],
                "cv_id": data.cv_id,
                "jd_id": data.jd_id,
                "question_context": question["question"],
                "topic": question["topic"],
                "interview_session_id": interview_session.id,
            }
            new_question_obj: Question = Question(**new_question_data)
            new_question = await create_question(new_question_obj, db)
            # Create ground truth texts from list of ground truths in Question
            ground_truths = question["ground_truths"]
            for gt in ground_truths:
                text: Text = Text(**{"text": gt, "parent_id": new_question.id})
                new_text = await create_text(text, db)
                logger.info(f"Created text with ID {new_text.id}")

    for cv_text in cv_texts:
        new_text_data_by_cv_data = {"parent_id": get_cv.id, "text": cv_text}
        new_text_data_by_cv_obj: Text = Text(**new_text_data_by_cv_data)
        await create_text(new_text_data_by_cv_obj, db)

    return {"interview_session_id": interview_session.id}


@router.post(
    "/send/question_selection", response_model=QuestionSelectionPipelineOutput
)
async def send_mlproxy_questionselection(
    data: QuestionSelectionPipelineInput, db: Session = Depends(get_db)
):
    # Read the question base on the question id
    input_question = await read_question(data.question_id, db)

    # Update the question attr is_used
    updated_input_question_dict = {
        k: v
        for k, v in input_question.__dict__.items()
        if not k.startswith("_")
    }
    updated_input_question_dict["is_used"] = True
    updated_input_question_dict["is_answered"] = data.is_answered
    updated_input_question = update_question(updated_input_question_dict, db)

    # Create an askedQuestion
    asked_question = createAskedQuestionObjectDict(updated_input_question)

    # Create Question
    question = createQuestionObjectDict(updated_input_question)
    
    # Get the question bank base on interview session
    question_bank_obj = (
        await get_all_questions_by_interviewer_id_and_interview_session_id(
            data.interviewer_id, data.interview_session_id, db
        )
    )

    # Create a question bank for ML
    question_bank_dict = createQuestionBankDict(question_bank_obj)

    # Create ML input data
    ml_input_data = createMLInput(question_bank_dict, asked_question)
    return_ml_data = await handle_send_question_selection(ml_input_data)
    return return_ml_data
