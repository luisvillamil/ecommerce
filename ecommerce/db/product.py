#!/bin/python

# base libraries
from uuid import UUID
# external libraries
from sqlmodel import select, Session, or_
from sqlalchemy.exc import IntegrityError

# internal libraries
from ecommerce.schemas import (
    Product, ProductCreate, Category, CategoryCreate)


# exports
__all__ = (
    "create_category",
    "get_category_by_id",
    "get_categories",
)

async def create_category(session:Session, category:CategoryCreate):
    """Creates new user in database"""
    # hash password before saving in db
    new_category = Category.model_validate(category)
    session.add(new_category)
    try:
        session.commit()
    except IntegrityError as e:
        raise ValueError("Category name or code already exists") from e
    session.refresh(new_category)
    return new_category

async def get_category_by_id(session:Session, _id:int):
    """Gets category by id

    Args:
        session (Session): database session
        _id (int): numerical identifier for category
    """
    return session.get(Category, {"id": _id})

async def get_categories(session:Session, offset:int, limit:int):
    categories = session.exec(
        select(Category).offset(offset).limit(limit)).all()
    return categories

async def create_product(session:Session, product:ProductCreate):
    new_product = Product.model_validate(product)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
