from pathlib import Path
from typing import Any

from schemas.search_schema import SearchSettings
from utils.check_normal_files import get_normal
from utils.check_zip_files import get_zip


def get_all_files(search_settings: SearchSettings, provided_path: str) -> dict[str, Any]:
    """ 
        Get list of all suitable file names in target directory and all subdirectories/zip-archives 
    """
    folder = Path(provided_path)

    normal_files = get_normal(folder, search_settings)
    zip_files = get_zip(folder, search_settings)

    return {"normal_files": normal_files, "zip_files": zip_files}
