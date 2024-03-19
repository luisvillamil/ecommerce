# default libraries
from typing import Annotated
from datetime import timedelta
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

# internal libraries
from ecommerce.config import settings
from ecommerce.db import db_client, authenticate_user
from ecommerce.schemas.user import User, UserRead
from ecommerce.schemas.token import Token
from ecommerce.core.security import create_access_token
from ecommerce.api.dependencies import (
    get_current_active_user,
    get_current_admin_user)

logger = logging.getLogger("uvicorn")
router = APIRouter()


@router.post("/token", response_model=Token)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(db_client.get_session)]):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/ping")
async def read_sub(_token: Annotated[str, Depends(get_current_admin_user)]):
    return {"message": "Hello World from admin"}

@router.get("/users/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
