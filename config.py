import os
import inspect

from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_TITLE: str = "KasperskyFileSearchSystem"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "A service that provide you possibilities to search files through your local file-system"

    TARGET_DIRECTORY: str = os.getenv("TARGET_DIRECTORY", "/")

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


settings = Settings()
