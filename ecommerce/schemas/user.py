"""User related schemas"""

# base libraries
from typing import Optional
from uuid import UUID, uuid4

# external libraries
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr

__all__ = (
    "UserBase",
    "UserCreate",
    "UserRead",
    "User")

class UserBase(SQLModel):
    """Base User model"""
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    full_name: str | None = None
class User(UserBase, table=True):
    """Full User model"""
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    password: str
    disabled: bool | None = None
    admin: bool | None = None

class UserCreate(UserBase):
    """Model to create user."""
    password: str
    admin: bool | None = None

class UserRead(UserBase):
    """Model to read user"""
    id: UUID



# class User(BaseModel):
#     """Full User model

#     Args:
#         BaseModel (_type_): _description_
#     """
#     username: str
#     email: EmailStr | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     """Parsed User from db with hashed password"""
#     hashed_password: str
