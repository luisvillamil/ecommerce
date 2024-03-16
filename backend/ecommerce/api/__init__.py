from fastapi import APIRouter

from ecommerce.api.endpoints import item, login, user, category, product

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(category.router, tags=["category"])
api_router.include_router(product.router, tags=["product"])
api_router.include_router(item.router, tags=["items"])
