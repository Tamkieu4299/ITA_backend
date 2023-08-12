import os
from typing import List, Optional
import uuid

from ..crud.user_crud import create_user,read_user,delete_user,get_users
from fastapi import APIRouter, Depends, status, Body
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..models.user_model import User
from ..services.validate_input import validate_input_included
from ..utils.exception import NotFoundException, InvalidInput
from ..schemas.user_schema import UserBaseSchema, UserResponse
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
	"",
	status_code=status.HTTP_201_CREATED,
	response_model=UserResponse,
)
async def register_user(
	user_data: UserBaseSchema,
	db: Session = Depends(get_db),
):
	"""Create an User"""
	user: User = User(**user_data.dict())
	new_user = create_user(user, db)

	# Check if the type input is valid
	isValid = validate_input_included(new_user.role, ["interviewer", "interviewee"])

	# Check if not valid
	if not isValid:
			raise InvalidInput(detail="The role should be interviewer/interviewee only")
	
	if (new_user is not None):
		logger.info(f"Created user {new_user.username} with ID {new_user.id}")
		return new_user.__dict__

	return new_user.__dict__

@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
	"""Get the user by its id"""
	user = read_user(id, db)

	if user is None:
			logger.info(f"Invalid user with ID: {id}")
			raise NotFoundException(detail=f"Invalid user with ID: {id}")

	logger.info(f"Get user with ID: {user.id}")
	return user.__dict__


@router.delete("/{id}", response_model=List[UserResponse])
async def delete_user_by_id(id: str, db: Session = Depends(get_db)):
	"""Delete user by its id"""
	result = delete_user(id, db)
	if not result:
			logger.info(f"Invalid user with ID: {id}")
			raise NotFoundException(detail=f"Invalid user with ID: {id}")

	logger.info(f"Deleted user with ID: {id}")
	users = get_all_users(db)
	users_dict_list = [i.__dict__ for i in users]
	return users_dict_list


@router.get("", response_model=List[UserResponse])
async def get_all_users(role: Optional[str] = None, db: Session = Depends(get_db)):
	"""Get all users"""
	
	# Check if the type input is valid
	isValid = validate_input_included(role, ["interviewer", "interviewee"])

	# Check if not valid
	if not isValid:
		raise InvalidInput(detail="The role should be interviewer/interviewee only")

	users = get_users(db, role)
	users_dict_list = [i.__dict__ for i in users]
	logger.info(f"Number of users: {len(users)}")
	return users_dict_list


