from fastapi import FastAPI

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

@app.get("/api/content")
async def get_content():
    return {"content": "This is the content of the API" }