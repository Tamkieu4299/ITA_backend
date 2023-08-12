import os
from typing import List
import uuid

from fastapi import APIRouter, Depends, Body
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.auth_crud import (
		authenticate_user
)
from ..db.database import get_db
from ..models.user_model import User
from ..schemas.user_schema import UserLogin, UserResponse
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

@router.post("/token", response_model = UserResponse)
async def login_for_access_token(user: UserLogin = Body(default=None), db: Session = Depends(get_db)):
	"""Authenticate user"""
	userDB = authenticate_user(user.username, user.password, db)
	if not userDB:
		return {'success': False, 'message': 'Invalid email or password'}
	return userDB.__dict__

@router.post("/logout")
async def logout():
	"""Logout user"""
	return {'success': True, 'message': 'Logout successfully'}



