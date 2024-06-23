# base libraries
import logging
from typing import Generator, Annotated

# external libraries
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from ecommerce.core import security
from ecommerce.config import settings
from ecommerce.db import db_client, get_user_by_username
from ecommerce.schemas.user import User
from ecommerce.schemas.token import TokenData

logger = logging.getLogger("uvicorn")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = f"{settings.API_VERSION}/token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(
        token: TokenDep,
        session: Annotated[Session, Depends(db_client.get_session)]):
    """Uses Oauth2 schema to get user model

    Args:
        token (Annotated[str, Depends): valid token for specified user

    Raises:
        credentials_exception: if credentials are not validated

    Returns:
        UserInDB: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    user = await get_user_by_username(session, username=token_data.username)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]):
    """Gets current user"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    """Checks wether user is admin"""
    if not current_user.admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
