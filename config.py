import os
import inspect
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_TITLE: str = "KasperskyFileSearchSystem"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "A service that provide you possibilities to search files through your local file-system"
    PROJECT_OPENAPI_URL: str = "/api/openapi.json"
    PROJECT_DOCS_URL: str = "/api/docs"

    DEPLOY: str = os.getenv("DEPLOY", "False")
    TARGET_DIRECTORY: str = os.getenv("TARGET_DIRECTORY", "/") if DEPLOY == "True" else str(Path(__file__).resolve().parent / "test_dir") 
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    
    POSTGRES_TEST_DB: str = os.getenv("POSTGRES_TEST_DB", "test_search_db")

    @property
    def project_settings(self) -> dict:
        """ Create a dictionary for unpacking into fastapi.FastAPI """
        attributes = inspect.getmembers(Settings)
        app_settings = {}
        for attr_name, attr_value in attributes:
            if attr_name.startswith("PROJECT_"):
                attr_name = attr_name.split("PROJECT_")[1].lower()
                app_settings.update({attr_name: attr_value})
        return app_settings

    @property
    def postgres_uri(self) -> str:
        """ Create a database URI for connection """
        uri = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return uri


settings = Settings()
