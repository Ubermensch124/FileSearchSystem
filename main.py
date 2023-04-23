from fastapi import FastAPI
from fastapi import Depends
import uvicorn

from config import settings
from utils.check_path import check_path
from api.routers import router
from db.connection import Base, engine


def db_init():
    Base.metadata.create_all(engine)


def application(_: None = Depends(db_init)) -> FastAPI:
    check_path(settings.TARGET_DIRECTORY)
    app_instance = FastAPI(**settings.project_settings)
    app_instance.include_router(router)

    return app_instance


app = application()


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=80, reload=True)
