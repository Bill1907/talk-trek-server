from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello() -> dict:
    return {"message": "Hello World"}