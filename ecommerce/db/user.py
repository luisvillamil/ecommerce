#!/bin/python

# base libraries
from uuid import UUID
# external libraries
from sqlmodel import select, Session

# internal libraries
from ecommerce.config import settings
from ecommerce.schemas import User, UserCreate
from ecommerce.core.security import get_password_hash, verify_password

# exports
__all__ = (
    "authenticate_user",
    "get_user_list_internal",
    "get_user_by_username",
    "get_user_by_id",
    "create_superuser",
    "create_user")

async def get_user_by_username(session:Session, username: str):
    """returns UserInDB model if user is in db"""
    stmt = select(User).where(
        User.username == username)
    user = session.exec(stmt).one_or_none()
    return user

async def get_user_by_id(session:Session, _id: str)-> User | None:
    """returns UserInDB model if user is in db"""
    stmt = select(User).where(
        User.id == UUID(_id))
    user = session.exec(stmt).one_or_none()
    return user

async def create_user(session:Session, user:UserCreate)->User:
    """Creates new user in database"""
    # hash password before saving in db
    user.password = get_password_hash(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

async def create_superuser(session:Session)->User:
    """to be called initially by database if app has never ran

    Args:
        session (Session): session to run

    Returns:
        User: created user
    """
    user = UserCreate(
        username = str(settings.FIRST_SUPERUSER),
        email = str(settings.FIRST_SUPERUSER),
        password = str(settings.FIRST_SUPERUSER_PASSWORD),
        admin = True)
    return await create_user(session, user)

async def authenticate_user(session:Session, username: str, password: str):
    """gets user and verifies password

    Args:
        session (Session): initialized database session
        username (str): username to check
        password (str): unhashed password

    Returns:
        _type_: user if it exists
    """
    user = await get_user_by_username(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def get_user_list_internal(session:Session, **kwargs):
    """To be used internally only. matches kwargs with user schema"""
    stmt = select(User)
    for k,v in kwargs.items():
        stmt = stmt.where(
            getattr(User, k) == v)
    return session.exec(stmt).all()
    