from fastapi import FastAPI

import os
os.chdir('../')
from database.mongodb import MongoDB

app = FastAPI()
mongo = MongoDB()

# EXAMPLE ROUTES
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
    # filter = {
    #     "time_publish": "19 hours ago",
    # }
    content = mongo.get_all_content_as_list()[:2]

    # Convert ObjectId to string
    for item in content:
        item["_id"] = str(item["_id"])

    print(content)

    return { "content": content }

