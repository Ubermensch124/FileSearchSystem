from fastapi import FastAPI
import uvicorn

from config import settings
from utils.check_path import check_path
from api.routers import router
from db.connection import Base, engine


def application() -> FastAPI:
    check_path(settings.TARGET_DIRECTORY)
    Base.metadata.create_all(engine)
    app_instance = FastAPI(**settings.project_settings)
    app_instance.include_router(router)

    return app_instance


app = application()


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=80, reload=True)
