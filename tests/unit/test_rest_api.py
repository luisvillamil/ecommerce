import pytest
from fastapi import status, Form
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from ecommerce.db import db_client
from ecommerce.main import app
from ecommerce.api.v1.dependencies import get_current_active_user
from ecommerce.schemas import User, Category
from ecommerce.config import settings
from ecommerce.core.security import get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    # setup connection to test database
    engine = create_engine(
        "postgresql+psycopg2://postgres:password@127.0.0.1/test_database",
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    # create admin user
    with Session(engine) as session:
        session.add(User(
            username="test_admin",
            email="",
            password=get_password_hash("test_123"),
            admin=True))
        session.commit()
    with Session(engine) as session:
        yield session
    # teardown test database
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    client = TestClient(app)
    app.dependency_overrides[db_client.get_session] = get_session_override
    yield client
    app.dependency_overrides.clear()

# def test_token():
#     response = client.post(
#         "/login/token"
#     )

def get_token(client:TestClient):
    response = client.post("/api/v1/token", data={
        "grant_type": "password",
        "username": "test_admin",
        "password": "test_123"
    })
    assert response.status_code == 200
    data = response.json()
    return f"Bearer {data['access_token']}"

@pytest.mark.asyncio
async def test_admin_ping(client:TestClient):
    response = client.get("/api/v1/ping")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_admin_ping_pass(client:TestClient):
    token = get_token(client)
    response = client.get("/api/v1/ping", headers={"Authorization": token})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_product(session:Session, client:TestClient):
    product = {
            "name": "test_product",
            "description": "test_description",
            "image_url": "http://localhost/hello.jpg",
            "category_id": 1,
            "product_attributes": [
                {
                    "name": "test_attribute"
                }]}
    # unauthorized
    response = client.post(
        "/api/v1/product",
        json=product)
    assert response.status_code == 401
    token = get_token(client)
    # no category
    response = client.post(
        "/api/v1/product",
        headers={"Authorization": token},
        json=product)
    assert response.status_code == 400
    # success
    data = response.json()
    session.add(Category(name="test_category", id=1))
    session.commit()
    response = client.post(
        "/api/v1/product",
        headers={"Authorization": token},
        json=product)
    assert response.status_code == 200

