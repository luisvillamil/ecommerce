#!/bin/python
"""Ecommerce app"""

# built-in libraries
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from ecommerce.config import settings
from ecommerce import db
from ecommerce import api
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

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url = None if settings.PRODUCTION is True else f"{settings.API_VERSION}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id
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

app.include_router(api.api_router, prefix=settings.API_VERSION)
