from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_content():
    response = client.get("/api/content")
    assert response.status_code == 200
    assert response.json() == {
        "content": "This is the content of the API"
    }
