import os

from pydantic import BaseSettings, DirectoryPath
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    TARGET_DIRECTORY: DirectoryPath = os.getenv("TARGET_DIRECTORY", "/")


settings = Settings()
