from fastapi import APIRouter

from ecommerce.api.v1.endpoints import login, items, user, category

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(category.router, tags=["category"])
