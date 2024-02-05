#!/bin/python
"""Product database functions"""

# base libraries
# external libraries
from sqlmodel import select, Session

# internal libraries
from ecommerce.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    Attribute)
from .category import get_category_by_id


# exports
__all__ = (
    "create_product",
    "get_product_by_id",
    "get_products",
    "get_product_by_name",
    "update_product",
    "delete_product"
)

async def create_product(
    session:Session, product:ProductCreate):
    """Creates Product in database"""
    category = await get_category_by_id(session, product.category_id)
    new_product = Product(
        name = product.name,
        description= product.description,
        image_url = product.image_url,
        category = category
    )
    if product.attributes:
        new_product.attributes = [
                Attribute(
                    name = attribute.name,
                    product = new_product
                ) for attribute in product.attributes
            ]
    session.add(new_product)
    session.add_all(new_product.attributes)
    session.commit()
    session.refresh(new_product)
    return new_product

async def get_product_by_id(session:Session, _id:int):
    """Returns product if found, else None

    Args:
        session (Session): database session
        _id (int): primary key of product
    """
    return session.get(Product, {"id": _id})

async def get_products(session:Session, offset:int, limit:int):
    """Gets list of categories"""
    categories = session.exec(
        select(Product).offset(offset).limit(limit)).all()
    return categories

async def get_product_by_name(session:Session, name:str):
    """Returns product if found, else None

    Args:
        session (Session): database session
        _id (int): primary key of product
    """
    stmt = select(Product).where(Product.name == name)
    return session.exec(stmt).one_or_none()

async def update_product(session:Session, _id:int, product:ProductUpdate):
    """Updates the product specific fields

    Args:
        session (Session): database session
        _id (int): product id
        product (ProductUpdate): fields to change from the product

    Raises:
        LookupError: if product is not found
    """
    db_product = await get_product_by_id(session, _id)
    if not db_product:
        raise LookupError(f"product {_id} not found.")
    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

async def delete_product(session:Session, _id:int):
    """Deletes product from database

    Args:
        session (Session): database session
        _id (int): id of product

    Raises:
        LookupError: if product not found
    """
    product = await get_product_by_id(session, _id)
    if not product:
        raise LookupError(f"product {_id} not found.")
    session.delete(product)
    session.commit()
