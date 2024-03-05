from time import time
from typing import Union
from typing_extensions import Annotated
from fastapi import Depends, UploadFile
from sqlmodel import Session
from ecommerce.file import get_storage, LocalStorage
from ecommerce.schemas import Product, Category, Item, Image


async def upload_image(
    file:UploadFile,
    db_object: Union[Product, Category, Item],
    session: Session):
    storage = get_storage()
    object_acronym = type(db_object).__name__.upper()[:3]
    current_time = time()
    filename = (f"{object_acronym}_{db_object.id}_"
                f"{current_time}_{file.filename}")
    file_path = await storage.upload(await file.read(), filename)
    new_image = Image(image_url=file_path)
    session.add(new_image)
    # if isinstance(db_object, Product):
    #     db_object = await db.get_product_by_id(session, db_object.id)
    db_object.images.append(new_image)
    session.commit()
