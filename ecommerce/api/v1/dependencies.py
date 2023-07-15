from typing import Generator, Annotated
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
# from sqlalchemy.orm import Session

# from app import crud, models, schemas
from ecommerce.core import security
from ecommerce.config import settings
from ecommerce.db import fake_users_db, get_user
from ecommerce.schemas.user import User
from ecommerce.schemas.token import TokenData
# from app.db.session import SessionLocal

logger = logging.getLogger("uvicorn")
# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = f"{settings.API_VERSION}/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> models.User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = schemas.TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = crud.user.get(db, id=token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_current_active_user(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user