from typing import Annotated
from datetime import timedelta
import logging

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ecommerce.config import settings
from ecommerce.db import fake_users_db
from ecommerce.schemas.user import UserInDB, User
from ecommerce.schemas.token import Token
from ecommerce.core.security import authenticate_user, create_access_token
from ecommerce.api.v1.dependencies import fake_hash_password, get_current_active_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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
def read_sub(token: Annotated[str, Depends(get_current_active_user)]):
    return {"message": "Hello World from admin"}

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
