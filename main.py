import os

from fastapi import FastAPI
import uvicorn

from config import settings


app = FastAPI()


@app.get("/")
def files():
    return {f"Objects at {settings.TARGET_DIRECTORY}": os.listdir(settings.TARGET_DIRECTORY)}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=80, reload=True)
