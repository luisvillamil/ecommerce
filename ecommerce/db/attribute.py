#!/bin/python
"""Database functions for attribute"""

# base libraries

# external libraries
from sqlmodel import Session
# internal libraries

from ecommerce.schemas import (
    AttributeCreate,
    AttributeValueCreate)
# exports
__all__ = (
    "create_attribute",
    "get_attribute",
    "create_attribute_value",
    "get_attribute_value"
)

async def create_attribute(session:Session, attribute:AttributeCreate):
    pass

async def get_attribute(session:Session, _id:int):
    pass

async def create_attribute_value(session:Session, attribute_value:AttributeValueCreate):
    pass

async def get_attribute_value(session:Session, _id:int):
    pass
