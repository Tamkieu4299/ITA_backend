import os
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.generation_crud import (
    check_video_type_exist,
    create_generation,
    delete_generation,
    get_all_base_generations,
    get_all_generations,
    get_all_generations_by_user,
    read_generation,
    update_generation,
    update_type_generation,
)
from ..db.database import get_db
from ..models.generation_model import Generation
from ..schemas.generation_schema import (
    GenerationBaseSchema,
    GenerationCheckTypeExist,
    GenerationResponse,
    GenerationUpdate,
    GenerationUpdateType,
)
from ..schemas.mlp_avatargeneration_schema import (
    MLPBaseAvatarGenerationSchema,
    MLPInputAvatarGenerationSchema,
)
from ..services.validate_data import validate_user_id
from ..services.validate_input import validate_input_included
from ..utils.exception import InvalidInput, NotFoundException
from ..utils.logger import setup_logger
from ..utils.avatar_generation_utils import (
    createGenerationObjectDict,
    sendGenerationML,
    receiveMLResponse,
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
    response_model=GenerationResponse,
)
async def add_generation(
    generation_data: GenerationBaseSchema = Depends(),
    db: Session = Depends(get_db),
):
    """Create the generation"""
    generation: Generation = Generation(**generation_data.dict())
    new_generation = await create_generation(
        generation, db, generation_data.dict()
    )

    logger.info(f"Created generation with ID {new_generation.id}")

    return new_generation.__dict__


@router.put("/update/", response_model=GenerationResponse)
async def update_generation_by_id(
    generation: GenerationUpdate, db: Session = Depends(get_db)
):
    """update the cv by its id"""
    generation_obj = await update_generation(generation.dict(), db)
    if generation_obj is None:
        logger.info(f"Invalid Generation with ID: {generation.id}")
        raise NotFoundException(
            detail=f"Invalid Generation with ID: {generation.id}"
        )

    logger.info(f"Update CV with ID: {generation_obj.id}")
    return generation_obj.__dict__


@router.put("/update_type/", response_model=GenerationResponse)
async def update_generation_type_by_user_id(
    generation: GenerationUpdateType, db: Session = Depends(get_db)
):
    """update the cv by its id"""
    # Check if the type input is valid
    isValid = validate_input_included(
        generation.type, ["base", "generated", "intro"]
    )

    # Check if not valid
    if not isValid:
        raise InvalidInput(
            detail="The type should be base/generated/intro only"
        )

    generation_obj = await update_type_generation(generation.dict(), db)
    if generation_obj is None:
        logger.info(f"Invalid Generation with user_ID: {generation.id}")
        raise NotFoundException(
            detail=f"Invalid Generation with user_ID: {generation.id}"
        )

    logger.info(f"Update CV with ID: {generation_obj.id}")
    return generation_obj.__dict__


@router.get("/get/{id}", response_model=GenerationResponse)
async def get_generation_by_id(id: str, db: Session = Depends(get_db)):
    """Get the generation by its id"""
    generation = await read_generation(id, db)

    if generation is None:
        logger.info(f"Invalid generation with ID: {id}")
        raise NotFoundException(detail=f"Invalid generation with ID: {id}")

    logger.info(f"Get generation with ID: {generation.id}")
    return generation.__dict__


@router.get("/delete/{id}", response_model=List[GenerationResponse])
async def delete_generation_by_id(id: str, db: Session = Depends(get_db)):
    """Delete generation by its id"""
    result = delete_generation(id, db)
    if not result:
        logger.info(f"Invalid generation with ID: {id}")
        raise NotFoundException(detail=f"Invalid generation with ID: {id}")

    logger.info(f"Deleted generation with ID: {id}")
    generations = get_all_generations(db)
    generations_dict_list = [i.__dict__ for i in generations]
    return generations_dict_list


@router.get("/", response_model=List[GenerationResponse])
async def get_generations(db: Session = Depends(get_db)):
    """Get all generations"""
    generations = await get_all_generations(db)
    generations_dict_list = [i.__dict__ for i in generations]
    logger.info(f"Number of generations: {len(generations)}")
    return generations_dict_list


@router.get("/base", response_model=List[GenerationResponse])
async def get_base_generations(db: Session = Depends(get_db)):
    """Get all base generations"""
    generations = await get_all_base_generations(db)
    generations_dict_list = [i.__dict__ for i in generations]
    logger.info(f"Number of base generations: {len(generations)}")
    return generations_dict_list


@router.post(
    "/check_video_type_exist", response_model=List[GenerationResponse]
)
async def get_video_type_exist(
    generation: GenerationCheckTypeExist, db: Session = Depends(get_db)
):
    """Get all base generations"""
    generations = await check_video_type_exist(
        generation.user_id, generation.type, db
    )
    generations_dict_list = [i.__dict__ for i in generations]
    logger.info(f"Number of base generations: {len(generations)}")
    return generations_dict_list


@router.get("/get_by_user/", response_model=List[GenerationResponse])
async def get_generations_by_user_id(
    user_id: str, type: Optional[str] = None, db: Session = Depends(get_db)
):
    """Get all generations by user id"""
    # Validate user_id
    if not validate_user_id(user_id, db):
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")

    generations = await get_all_generations_by_user(user_id, db, type)
    generations_dict_list = [i.__dict__ for i in generations]
    logger.info(f"Get generations with user_id: {user_id}")
    return generations_dict_list


@router.post("/send/talking_head")
async def send_mlproxy_talkinghead(
    data: MLPBaseAvatarGenerationSchema,
):
    """Send message to ML proxy to render video"""
    # Create the input data for ML
    input_data = createGenerationObjectDict(data.dict())

    # Send data to ML and receive response
    # response_ml = await sendGenerationML(input_data)
    response_ml = {
        "status": True,
        "data": {
            "status": "SUCCESS",
            "task_id": input_data["task_id"],
            "Detail": "Send successfully",
        },
    }
    if not response_ml["status"]:
        return response_ml["data"]

    if response_ml["data"]["status"] != "SUCCESS":
        response_ml["data"]["Detail"]

    return response_ml["data"]["status"]


@router.post("/receive/talking_head")
async def receive_mlproxy_talkinghead(
    data: MLPInputAvatarGenerationSchema, db: Session = Depends(get_db)
):
    """Receive data from ML proxy to render video"""
    response_server = await receiveMLResponse(data.dict(), db)
    return response_server
