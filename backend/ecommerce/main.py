#!/bin/python
"""Ecommerce app"""

# built-in libraries
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ecommerce.config import settings
from ecommerce import db
from ecommerce.api import v1
# from app.core.config import settings

@asynccontextmanager
async def lifespan(_app: FastAPI):
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
    lifespan=lifespan,
    openapi_url = None if settings.PRODUCTION is True else f"{settings.API_VERSION}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(v1.api_router, prefix=settings.API_VERSION)