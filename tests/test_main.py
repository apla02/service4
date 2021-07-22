
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



client = TestClient(app)
"""Define an instance of Testclient using the FastAPI app"""


def test_home():
    """ Testing to check if browser is working with method get"""
    response = client.get("/")
    assert response.status_code == 200
