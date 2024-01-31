# default libraries
from typing import Annotated, List
from datetime import timedelta
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlmodel import Session
# internal libraries
from ecommerce.db import (
    db_client, create_category, get_categories, get_category_by_id)
from ecommerce.schemas.product import (
    CategoryRead, CategoryCreate, CategoryReadWithProducts)
from ecommerce.api.v1.dependencies import get_current_active_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/category", response_model=CategoryRead)
async def post_category(
    _token: Annotated[str, Depends(get_current_active_user)],
    new_category:CategoryCreate, session:Session=Depends(db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        category = await create_category(session, new_category)
        return category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)) from e

@router.get("/category", response_model=CategoryReadWithProducts)
async def get_category_endpoint(
    _id:int, session:Session=Depends(db_client.get_session)):
    try:
        category = await get_category_by_id(session, _id)
        return category
    except LookupError as e:
        raise HTTPException(
            status_code=404, detail=str(e)) from e

@router.get("/category/list", response_model=List[CategoryRead])
async def get_category_list_endpoint(
    session:Session=Depends(db_client.get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)):
    categories = await get_categories(session, offset, limit)
    return categories
