from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404  # Since no root endpoint, expect 404

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200