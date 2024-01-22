#!/bin/python
"""Ecommerce app"""

# built-in libraries
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

from ecommerce.config import settings
from ecommerce import db
from ecommerce.api.v1 import api_router
# from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Determines what will happen during the lifespan of app

    Args:
        app (FastAPI): app to run
    """
    # start db
    await db.db_client.run()
    yield
    # cleanup
    await db.db_client.cleanup()



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(api_router, prefix=settings.API_VERSION)
