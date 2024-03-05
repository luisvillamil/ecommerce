#!/bin/python
"""Database functions for attribute"""

# base libraries
import time
import random
# external libraries
from sqlmodel import Session, select
# internal libraries

from ecommerce.schemas import (
    Item,
    ItemCreate,
    ItemUpdate,
    Product,
    AttributeValue)
# exports
__all__ = (
    "create_item",
    "get_item",
    "delete_item",
    "update_item",
    "get_item_list"
)


async def create_item(session:Session, item:ItemCreate):
    """Creates Item in database. Assumes product and category have been created

    Args:
        session (Session): database session
        item (ItemCreate): item to create

    Raises:
        LookupError: if no product associated is found
    """
    stmt = select(Product).where(
        Product.id == item.product_id)
    product = session.exec(stmt).one_or_none()
    if not product:
        raise LookupError("Product not found")
    new_item = Item(
        name=item.name,
        stock_quantity=item.stock_quantity,
        price=item.price,
        product=product)
    session.add(new_item)
    if item.attribute_values:
        new_item.attribute_values = [
            AttributeValue(
                value=attr.value,
                attribute_id=attr.attribute_id,
                item=new_item
            )
            for attr in item.attribute_values]
    session.add_all(new_item.attribute_values)
    generate_sku(
        new_item,
        product.category.name[:3].upper(),
        product.name[:3].upper())
    session.commit()
    session.refresh(new_item)
    return new_item

async def get_item(session:Session, _id:int):
    """Gets item from database. None if not found"""
    return session.get(Item, {"id": _id})

async def get_item_list(session:Session, offset:int, limit:int):
    """Gets item list from database"""
    stmt = select(Item).offset(offset).limit(limit)
    return session.exec(stmt).all()

async def delete_item(session:Session, _id:int):
    """deletes item from database."""
    item = await get_item(session, _id)
    if not item:
        raise LookupError(f"item {_id} not found.")
    session.delete(item)
    session.commit()

async def update_item(session:Session, _id:int, item_update:ItemUpdate):
    """Updates item from database."""
    db_item = await get_item(session, _id)
    if not db_item:
        raise LookupError(f"Item {_id} not found.")
    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def generate_sku(item:Item, cat_name:str, prod_name:str):
    """
        Generates a unique SKU for a product.
        :param product: A short code representing the product category.
        :return: A unique SKU string.
    """
    # Current time in milliseconds (used for uniqueness)
    timestamp = int(time.time() * 1000)

    # Random number for additional uniqueness
    random_number = random.randint(100, 999)
    attr_names = "-"
    attr_names = "-" + "-".join(
        [attr.value[:3].upper() for attr in item.attribute_values]) + "-"

    # Combine elements to form SKU
    sku = f"{cat_name}-{prod_name}{attr_names}{timestamp}-{random_number}"
    item.sku = sku
