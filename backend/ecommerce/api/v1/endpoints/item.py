"""Items CRUD"""

from typing import Annotated, List
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlmodel import Session

# internal libraries
from ecommerce import db
from ecommerce.schemas import ItemCreate, ItemRead, ItemUpdate
from ecommerce.api.v1.dependencies import get_current_admin_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.get("/item/list", response_model=List[ItemRead])
async def get_item_list(*,
    session:Session=Depends(db.db_client.get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)):
    """gets item list"""
    return await db.get_item_list(session, offset, limit)

@router.post("/item", response_model=ItemRead)
async def post_item(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session),
    new_item:ItemCreate):
    """Creates item"""
    try:
        item = await db.create_item(session, new_item)
        return item
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e)) from e

@router.get("/item", response_model=ItemRead)
async def get_item(*,
    session:Session=Depends(db.db_client.get_session),
    _id:int):
    """Gets item by specified _id"""
    item = await db.get_item(session, _id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"item {_id} not found.")
    return item

@router.put("/item", response_model=ItemRead)
async def update_item(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session),
    _id:int,
    item:ItemUpdate):
    """Updates item specified by id"""
    try:
        item = await db.update_item(session, _id, item)
        return item
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"item {_id} not found.") from e

@router.delete("/item")
async def delete_item(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session),
    _id:int):
    """Deletes item specified by id"""
    try:
        await db.delete_item(session, _id)
        return {"message": "item deleted"}
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"item {_id} not found.") from e
