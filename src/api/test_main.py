# from fastapi.testclient import TestClient

# from .main import app

# client = TestClient(app)


# def test_get_content():
#     response = client.get("/api/content")
#     assert response.status_code == 200
#     assert response.json() == {
#         "content": "content"
#     }

# def test_say_hello():
#     name = "peter"
#     response = client.get(f"hello/{name}")
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": f"Hello {name}"
#     }

