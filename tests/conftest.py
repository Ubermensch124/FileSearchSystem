import os
from pathlib import Path
import shutil
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, drop_database, database_exists

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from config import settings
from db.connection import Base, get_session
from tests.data import data_example
from utils.create_test_dir import create_test_dir


TEST_DIRECTORY = Path(__file__).resolve().parent.parent / "test_dir"
TEST_DB_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_TEST_DB}"

engine = create_engine(TEST_DB_URI)
if database_exists(engine.url):
    drop_database(engine.url)
create_database(engine.url)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def data():
    return data_example


@pytest.fixture(scope="session", autouse=True)
def prepare_files_and_db():    
    create_test_dir(TEST_DIRECTORY=TEST_DIRECTORY)
    yield
    shutil.rmtree(TEST_DIRECTORY)
    drop_database(engine.url)


def test_get_session():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def session():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = test_get_session


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client
