import aiohttp
from sqlalchemy.orm import Session

from ..crud.cv_crud import update_cv
from ..crud.answer_crud import update_answer
import random  # this is for local test
from ..utils.avatar_generation_utils import receiveMLResponse, sendGenerationML


async def handle_return_mlp_avatargeneration(input_data: dict, db: Session):
    # response_ml = sendGenerationML(input_data)
    # if not response_ml["status"]:
    #     return None
    # response_data = response_ml["data"]
    response_data = {
        "task_id": input_data["task_id"],
        "video_url": {
            "bucket": "ita-test-01",
            "key_file": "hungnguyendc-storage-01/outputs/VideoRetalking/a2ea8de1-a4a1-4c05-abe1-b89f881e83d7.mp4",
        },
    }
    response_server = await receiveMLResponse(response_data, db)
    return response_server


async def handle_send_cv_mlproxy(input_data: dict, db: Session):
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         settings.CV_EXTRACTING_URL,
    #         json=input_data,
    #     ) as response:
    #         response_data = await response.json()

    #     # Update the CV schema
    #     updated_cv = update_cv(response_data, db)
    #     return updated_cv.__dict__
    response_data = "[{'page': '1', 'sections': 'Sample data'}]"
    updated_data_obj = {"cv_id": input_data["cv_id"], "texts": response_data}
    update_cv(updated_data_obj, db)
    return response_data


async def handle_send_question_generation(input_data: dict):
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         settings.QUESTION_GENERATION_URL,
    #         json=input_data,
    #     ) as response:
    #         response_data = await response.json()

    #     return response_data
    response_data = {
        "task_id": input_data["id"],
        "questions": [
            {
                "question": "How are you today ?",
                "ground_truths": [
                    "Sample ground 1",
                    "Sample ground 2",
                    "Sample ground 3",
                ],
                "topic": 1,
            },
            {
                "question": "How old are you ?",
                "ground_truths": [
                    "Sample ground 1",
                    "Sample ground 2",
                    "Sample ground 3",
                ],
                "topic": 2,
            },
            {
                "question": "What are your strengths and weakness?",
                "ground_truths": [
                    "Sample ground 1",
                    "Sample ground 2",
                    "Sample ground 3",
                ],
                "topic": 3,
            },
        ],
        "cv_texts": [
            "Dummy CV texts 1",
            "Dummy CV texts 2",
            "Dummy CV texts 3",
            "Dummy CV texts 4",
        ],
    }
    return response_data


async def handle_send_question_selection(input_data: dict):
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         settings.QUESTION_SELECTION_URL,
    #         json=input_data,
    #     ) as response:
    #         response_data = await response.json()

    #     return response_data
    questions = input_data["question_bank"]
    return {"question_id": random.choice(questions)["question_id"]}


async def handle_send_answer_analysis(input_data: dict, db: Session):
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         settings.QUESTION_SELECTION_URL,
    #         json=input_data,
    #     ) as response:
    #         response_data = await response.json()

    #     return response_data
    response = {
        "task_id": input_data["task_id"],
        "overall_score": 0.8,
        "confidence_score": 0.9,
        "text_relevancy_score": 0.75,
        "has_bad_words": False,
        "professional_score": 0.85,
        "emotion_from_text": "happy",
        "emotion_from_audio": "calm",
        "emotion_from_video": "excited",
    }

    update_answer_dict = {
        k: v for k, v in response.items() if not k == "task_id"
    }
    update_answer_dict["id"] = input_data["task_id"]
    updated_answer = update_answer(update_answer_dict, db)
    return response
