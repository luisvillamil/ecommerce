# default libraries
from typing import Annotated, Optional, List
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status
from sqlmodel import Session
# internal libraries
from ecommerce.db import (
    db_client,
    create_product,
    get_product_by_id,
    get_product_by_name,
    update_product,
    delete_product)
from ecommerce.schemas.product import (
    ProductReadWithAttributes, ProductCreate, ProductUpdate, ProductAttributeCreate)
from ecommerce.api.v1.dependencies import get_current_active_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/product", response_model=ProductReadWithAttributes)
async def post_product(*,
    _token: Annotated[str, Depends(get_current_active_user)],
    session:Session=Depends(db_client.get_session),
    new_product:ProductCreate):
    """creates category from defined schema. Admin only"""
    # print(new_product, product_attributes)
    try:
        category = await create_product(session, new_product)
        return category
    except (ValueError, LookupError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)) from e

@router.get("/product", response_model=ProductReadWithAttributes)
async def get_product(*,
    _id:int, session:Session=Depends(db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        category = await get_product_by_id(session, _id)
        return category
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e

@router.get("/product/name", response_model=ProductReadWithAttributes)
async def get_product_by_name_endpoint(*,
    name:str, session:Session=Depends(db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        product = await get_product_by_name(session, name)
        return product
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e

@router.put("/product", response_model=ProductReadWithAttributes)
async def put_product(*,
    _token: Annotated[str, Depends(get_current_active_user)],
    _id:str, product: ProductUpdate, 
    session:Session=Depends(db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        product = await update_product(session, _id, product)
        return product
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e

@router.delete("/product")
async def delete_product_endpoint(*,
    _token: Annotated[str, Depends(get_current_active_user)],
    _id:str, session:Session=Depends(db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        await delete_product(session, _id)
        return {"ok": True}
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e
