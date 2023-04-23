import uvicorn
from fastapi import FastAPI
from sqlalchemy_utils.functions import database_exists, create_database

from config import settings
from utils.check_path import check_path
from api.routers import router
from db.connection import Base, engine


def db_init():
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


def application() -> FastAPI:
    check_path(settings.TARGET_DIRECTORY)
    db_init()
    app_instance = FastAPI(**settings.project_settings)
    app_instance.include_router(router)

    return app_instance


app = application()


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=80, reload=True)
