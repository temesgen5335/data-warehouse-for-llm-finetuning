from fastapi import FastAPI
from src.mongo_db import get_collection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/hello/user_{name}/{user_id}")
async def say_hello(user_id: int, name: str):
    response = {
        "message": f"Hello {name}",
        "user_id": f"{user_id}"
    }
    return response

# EDIT FROM HERE
@app.get("/api/content")
async def get_content():
    # Get content from MongoDB
    # collection = get_collection()

    return {"content": "content" }

