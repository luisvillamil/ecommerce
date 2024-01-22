from fastapi.testclient import TestClient
from ecommerce.main import app

client = TestClient(app)

# def test_token():
#     response = client.post(
#         "/login/token"
#     )

def test_admin_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 401


