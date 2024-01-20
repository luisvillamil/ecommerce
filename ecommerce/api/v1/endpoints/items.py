# products CRUD
from typing import Annotated
from datetime import timedelta
import logging

# external libraries
from fastapi import Depends, APIRouter, HTTPException, status

# internal libraries
from ecommerce.api.v1.dependencies import get_current_active_user

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.get("/product/list")
async def get_item_list():
    return {
        "product": ""
        }

@router.post("/product")
async def post_item(token: Annotated[str, Depends(get_current_active_user)]):
    return {"message": "item posted"}

@router.get("/product")
async def get_item():
    return {"message": "item"}

@router.put("/product")
async def update_item(token: Annotated[str, Depends(get_current_active_user)]):
    return {"message": "item updated"}

@router.delete("/product")
async def delete_item(token: Annotated[str, Depends(get_current_active_user)]):
    return {"message": "item deleted"}
