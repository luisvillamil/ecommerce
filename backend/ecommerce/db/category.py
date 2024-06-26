#!/bin/python

# external libraries
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError, NoResultFound

# internal libraries
from ecommerce.schemas import Category, CategoryCreate


# exports
__all__ = (
    "create_category",
    "get_category_by_id",
    "get_categories",
    "delete_category",
)

async def create_category(session:Session, category:CategoryCreate):
    """Creates new user in database"""
    # hash password before saving in db
    new_category = Category.model_validate(category)
    session.add(new_category)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ValueError("Category name or code already exists") from e
    session.refresh(new_category)
    return new_category

async def get_category_by_id(session:Session, _id:int):
    """Gets category by id

    Args:
        session (Session): database session
        _id (int): numerical identifier for category
    """
    category = session.get(Category, {"id": _id})
    if not category:
        raise LookupError(f"no category {_id} found")
    return category

async def get_categories(session:Session, offset:int, limit:int):
    """Gets list of categories"""
    categories = session.exec(
        select(Category).offset(offset).limit(limit)).all()
    return categories

async def delete_category(session:Session, _id:int):
    """deletes category by _id. if not found raises LookupError
        should cascade all deletes to products

    Args:
        session (Session): database session
        _id (int): id of category
    """
    category = await get_category_by_id(session, _id)
    session.delete(category)
    session.commit()
