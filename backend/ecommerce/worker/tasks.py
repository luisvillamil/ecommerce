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
    db_object.images.append(new_image)
    session.commit()
    session.refresh(new_image)
    return new_image

async def delete_image(
    file_obj: Image,
    db_object: Union[Product, Category, Item],
    session: Session):
    storage = get_storage()
    await storage.delete(file_obj.image_url)
    db_object.images.remove(file_obj)
    session.add(file_obj)
    session.delete(file_obj)
    session.commit()
