# default libraries
from typing import Annotated
import logging

# external libraries
from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    BackgroundTasks)
from sqlmodel import Session
# internal libraries
from ecommerce import db
from ecommerce.api.dependencies import get_current_admin_user
from ecommerce.worker.tasks import upload_image, delete_image
from ecommerce.schemas.product import ImageRead

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/image", response_model=ImageRead)
async def post_image(*,
    upload_file:UploadFile,
    object_type:str,
    _id: int,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session)):
    """Uploads image, adds it directly to product"""
    sesh_object = None
    if object_type == 'product':
        sesh_object = await db.get_product_by_id(session, _id)
    elif object_type == 'category':
        sesh_object = await db.get_category_by_id(session, _id)
    elif object_type == 'item':
        sesh_object = await db.get_item(session, _id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{object_type} not allowed.')
    if not sesh_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{object_type} {_id} not found')
    image = await upload_image(upload_file, sesh_object, session)
    return image

@router.delete("/image")
async def delete_image_endpoint(*,
    image_id: int,
    object_id: int,
    object_type: str,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session)):
    """Uploads image, adds it directly to product"""
    try:
        file_obj, sesh_obj = await db.get_image_by_id(
            session, image_id, object_id, object_type)
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    await delete_image(file_obj, sesh_obj, session)
    return f"Image {object_id} deleted."
