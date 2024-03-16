# default libraries
from typing import Annotated, Optional, List
import logging

# external libraries
from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    Query,
    UploadFile,
    BackgroundTasks)
from sqlmodel import Session
# internal libraries
from ecommerce import db
from ecommerce.schemas import (
    ProductReadWithItems,
    ProductReadWithAttributes,
    ProductCreate,
    ProductUpdate)
from ecommerce.api.dependencies import get_current_admin_user
from ecommerce.worker.tasks import upload_image

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/product", response_model=ProductReadWithAttributes)
async def post_product(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session),
    new_product:ProductCreate):
    """creates category from defined schema. Admin only"""
    # print(new_product, product_attributes)
    try:
        category = await db.create_product(session, new_product)
        return category
    except (ValueError, LookupError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)) from e

@router.post("/product/image")
async def post_image(*,
    file:UploadFile,
    _id: int,
    _token: Annotated[str, Depends(get_current_admin_user)],
    session:Session=Depends(db.db_client.get_session)):
    """Uploads image, adds it directly to product"""
    # check product exists
    product = await db.get_product_by_id(session, _id)
    if not product:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'product {_id} not found')
    img_url = await upload_image(file, product, session)
    # background_tasks.add_task(upload_image, file, contents, product)
    return "file accepted"

@router.get("/product", response_model=ProductReadWithAttributes)
async def get_product(*,
    _id:int, session:Session=Depends(db.db_client.get_session)):
    """creates category from defined schema. Admin only"""
    product = await db.get_product_by_id(session, _id)
    if not product:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'product {_id} not found')
    return product

@router.get("/product/name", response_model=ProductReadWithAttributes)
async def get_product_by_name(*,
    name:str, session:Session=Depends(db.db_client.get_session)):
    """creates category from defined schema. Admin only"""
    product = await db.get_product_by_name(session, name)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'product {name} not found')
    return product

@router.put("/product", response_model=ProductReadWithAttributes)
async def put_product(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    _id:str, product: ProductUpdate,
    session:Session=Depends(db.db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        product = await db.update_product(session, _id, product)
        return product
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e

@router.delete("/product")
async def delete_product(*,
    _token: Annotated[str, Depends(get_current_admin_user)],
    _id:str, session:Session=Depends(db.db_client.get_session)):
    """creates category from defined schema. Admin only"""
    try:
        await db.delete_product(session, _id)
        return {"ok": True}
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)) from e

@router.get("/product/list", response_model=List[ProductReadWithItems])
async def get_product_list(
    session:Session=Depends(db.db_client.get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)):
    """Gets list of products with items

    Args:
        offset (int, optional): page offset. Defaults to 0.
        limit (int, optional): number of products per page. Defaults to Query(default=100, le=100).
    """
    products = await db.get_products(session, offset, limit)
    return products
