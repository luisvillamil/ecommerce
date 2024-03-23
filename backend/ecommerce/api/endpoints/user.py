# default libraries
from typing import Annotated
from datetime import timedelta
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
# internal libraries
from ecommerce.db import db_client, create_user, get_user_by_id
from ecommerce.schemas.user import User, UserCreate, UserRead
from ecommerce.api.dependencies import get_current_active_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/user", response_model=UserRead)
async def create_user_endpoint(
    new_user:UserCreate, session:Session=Depends(db_client.get_session)):
    return await create_user(session, new_user)

@router.get("/user", response_model=UserRead)
async def get_user_endpoint(
    _id:str, session:Session=Depends(db_client.get_session)):
    user = await get_user_by_id(session, _id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.put("/user", response_model=UserRead)
async def update_user_endpoint(_id:str, **kwargs):
    pass

@router.delete("/user")
async def delete_user_endpoint(_id:str):
    pass

@router.get("/users/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
