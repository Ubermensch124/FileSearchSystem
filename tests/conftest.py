import os
from pathlib import Path
import shutil
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from config import settings
from db.connection import Base, get_session
from tests.data import data_example


TEST_DIRECTORY = Path(__file__).resolve().parent.parent / "test_dir"
TEST_DB_URI = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_TEST_DB}"


@pytest.fixture(scope="session")
def data():
    return data_example


@pytest.fixture(scope="session", autouse=True)
def create_files():
    os.mkdir(TEST_DIRECTORY)
    file_names = ["test1.txt", "test2.txt"]
    with open(TEST_DIRECTORY / file_names[0], "w+", encoding="utf-8") as file:
        file.write("abracadabra")
    with open(TEST_DIRECTORY / file_names[1], "w+", encoding="utf-8") as file:
        file.write("abr")
    
    yield
    shutil.rmtree(TEST_DIRECTORY)


engine = create_engine(TEST_DB_URI)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


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
