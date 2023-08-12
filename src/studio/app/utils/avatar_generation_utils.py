from ..crud.generation_crud import update_generation
from sqlalchemy.orm import Session
from ..constants.config import settings
import aiohttp


def createGenerationObjectDict(data: dict) -> dict:
    input_data = {"task_id": data["task_id"]}
    if data["video_key"]:
        video_url = {}
        video_url["bucket"] = data["bucket_name"]
        video_url["key_file"] = data["video_key"]
        input_data["video_url"] = video_url

    if data["audio_key"]:
        audio_url = {}
        audio_url["bucket"] = data["bucket_name"]
        audio_url["key_file"] = data["audio_key"]
        input_data["audio_url"] = audio_url

    if data["image_key"]:
        image_url = {}
        image_url["bucket"] = data["bucket_name"]
        image_url["key_file"] = data["image_key"]
        input_data["image_url"] = image_url

    if data["text"]:
        input_data["text"] = data["text"]

    return input_data


async def sendGenerationML(input_data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                settings.TALKING_HEAD_GENERATION_URL
                if not input_data["text"]
                else settings.TALKING_HEAD_GENERATION_WITH_TEXT_URL,
                json=input_data,
            ) as response:
                response_data = await response.json()
                return {"status": True, "data": response_data}
        except aiohttp.ClientError as e:
            return {"status": False, "data": e}


async def receiveMLResponse(response: dict, db: Session) -> dict:
    generation_dict = {"id": response["task_id"]}
    generation_dict["bucket_s3"] = response["video_url"]["bucket"]
    generation_dict["path_s3"] = response["video_url"]["key_file"]
    generation = await update_generation(generation_dict, db)
    return generation.__dict__
