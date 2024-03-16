import pytest
from fastapi import status, Form
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from ecommerce.db import db_client
from ecommerce.main import app
from ecommerce.schemas import User, Category, Product, Attribute
from ecommerce.config import settings
from ecommerce.core.security import get_password_hash

API_VERSION = settings.API_VERSION

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

def get_token(client:TestClient):
    response = client.post(f"{API_VERSION}/token", data={
        "grant_type": "password",
        "username": "test_admin",
        "password": "test_123"
    })
    assert response.status_code == 200
    data = response.json()
    return f"Bearer {data['access_token']}"

@pytest.mark.asyncio
async def test_admin_ping(client:TestClient):
    response = client.get(f"{API_VERSION}/ping")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_admin_ping_pass(client:TestClient):
    token = get_token(client)
    response = client.get(
        f"{API_VERSION}/ping", headers={"Authorization": token})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_category(client:TestClient):
    category = {"name": "test_category"}
    # unauthorized
    response = client.post(f"{API_VERSION}/category", json=category)
    assert response.status_code == 401
    token = get_token(client)
    # success
    response = client.post(
        f"{API_VERSION}/category",
        headers={"Authorization": token}, json=category)
    assert response.status_code == 200
    data = response.json()
    # value error
    response = client.post(
        f"{API_VERSION}/category",
        headers={"Authorization": token}, json=category)
    assert response.status_code == 400
    # delete category
    response = client.delete(
        f"{API_VERSION}/category",
        params={"_id": data["id"]})
    assert response.status_code == 200
    # delete category
    response = client.delete(
        f"{API_VERSION}/category",
        params={"_id": data["id"]})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_categories(session:Session, client:TestClient):
    # category = {"name": "test_category"}
    response = client.get(f"{API_VERSION}/category", params={'_id': 1})
    assert response.status_code == 404
    session.add(Category(name="test_category", id=1))
    response = client.get(f"{API_VERSION}/category", params={'_id': 1})
    assert response.status_code == 200
    response = client.get(f"{API_VERSION}/category/list")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_product(session:Session, client:TestClient):
    def test_gets(_id:str, name:str, code:int):
        response = client.get(f"{API_VERSION}/product", params={'_id': _id})
        assert response.status_code == code
        response = client.get(
            f"{API_VERSION}/product/name", params={"name": name})
        assert response.status_code == code
    test_gets(1, "test_product", 404)
    product = {
            "name": "test_product",
            "description": "test_description",
            "category_id": 1,
            "attributes": [
                {
                    "name": "test_attribute"
                }]}
    # unauthorized
    response = client.post(
        f"{API_VERSION}/product",
        json=product)
    assert response.status_code == 401
    headers = {"Authorization": get_token(client)}
    # no category
    response = client.post(
        f"{API_VERSION}/product",
        headers=headers,
        json=product)
    assert response.status_code == 400
    # success
    session.add(Category(name="test_category", id=1))
    session.commit()
    response = client.post(
        f"{API_VERSION}/product",
        headers=headers,
        json=product)
    assert response.status_code == 200
    data = response.json()
    # success get
    test_gets(data["id"], "test_product", 200)
    # update product
    response = client.put(
        f"{API_VERSION}/product",
        headers=headers,
        params={"_id": 3},
        json={ "name": "changed_product" })
    assert response.status_code == 404
    # update product
    response = client.put(
        f"{API_VERSION}/product",
        headers=headers,
        params={"_id": data["id"]},
        json={ "name": "changed_product" })
    assert response.status_code == 200
    # delete product
    response = client.delete(
        f"{API_VERSION}/product",
        headers=headers,
        params={"_id": data["id"]})
    assert response.status_code == 200
    # delete product
    response = client.delete(
        f"{API_VERSION}/product",
        headers=headers,
        params={"_id": data["id"]})
    assert response.status_code == 404
    # get product list
    response = client.get(
        f"{API_VERSION}/product/list")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_items(session:Session, client:TestClient):
    item = {
        "name": "test_item",
        "stock_quantity": 123,
        "product_id": 1,
        "price": 12,
        "attribute_values": [
            {
            "value": "test_value",
            "attribute_id": 1
            }
        ]
    }
    response = client.get(
        f"{API_VERSION}/item", params={"_id": 1})
    assert response.status_code == 404
    response = client.post(f"{API_VERSION}/item", json = item)
    assert response.status_code == 401
    headers = {"Authorization": get_token(client)}
    response = client.post(
        f"{API_VERSION}/item", headers = headers, json = item)
    assert response.status_code == 400
    cat = Category(name="test_category", id=1)
    product = Product(name="test_product", description="", image_url="",
                      category=cat, id=1)
    attribute = Attribute(name="test", id=1, product=product)
    product.attributes.append(attribute)
    session.add_all([cat, product, attribute])
    # success
    response = client.post(
        f"{API_VERSION}/item", headers = headers, json = item)
    assert response.status_code == 200
    data = response.json()
    response = client.get(
        f"{API_VERSION}/item", params={"_id": data["id"]})
    assert response.status_code == 200
    response = client.put(
        f"{API_VERSION}/item", params={"_id": data["id"]},
        headers=headers,
        json= {"name": "new_name"})
    assert response.status_code == 200
    response = client.delete(
        f"{API_VERSION}/item", headers=headers, params={"_id": data["id"]})
    assert response.status_code == 200
    response = client.delete(
        f"{API_VERSION}/item", headers=headers, params={"_id": data["id"]})
    assert response.status_code == 404
    response = client.put(
        f"{API_VERSION}/item", params={"_id": data["id"]},
        headers=headers,
        json= {"name": "new_name"})
    assert response.status_code == 404
    response = client.get(
        f"{API_VERSION}/item/list")
    assert response.status_code == 200
    assert response.json() == []
