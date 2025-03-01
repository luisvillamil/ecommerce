#!/bin/python
"""Image db functions"""
from typing import Tuple, Union
# external libraries
from sqlmodel import Session

# internal libraries
from ecommerce.schemas import Image, Product, Item, Category


# exports
__all__ = (
    "get_image_by_id",
)

allowed_objects = {
    "product": Product,
    "item": Item,
    "category": Category
}

async def get_image_by_id(
        session:Session,
        image_id:int,
        object_id:int,
        object_type:str
    )->Tuple[Image, Union[Product, Item, Category]]:
    """Gets image by id

    Args:
        session (Session): database session
        _id (int): numerical identifier for category
    """
    if object_type not in allowed_objects:
        raise ValueError(f'{object_type} not in allowed object types.')
    img_obj = session.get(Image, {"id": image_id})
    obj = session.get(allowed_objects[object_type], {"id": object_id})
    if not obj:
        raise LookupError(f'no {object_type} {object_id} found.')
    if not img_obj:
        raise LookupError(f"no image {image_id} found")
    return img_obj, obj
