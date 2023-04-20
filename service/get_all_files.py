from pathlib import Path
from typing import Any

from schemas.search_schema import SearchSettings
from utils.check_normal_files import get_normal
from utils.check_zip_files import get_zip


def get_all_files(search_settings: SearchSettings, provided_path: str) -> dict[str, Any]:
    """ Get list of all file names in target directory and all subdirectories/zip-archives """
    folder = Path(provided_path)

    file_mask = search_settings.file_mask
    size_value = search_settings.size.value
    size_operator = search_settings.size.operator
    creation_time_value = search_settings.creation_time.value
    creation_time_operator = search_settings.creation_time.operator

    normal_files = get_normal(folder, file_mask, size_value, size_operator, creation_time_value, creation_time_operator)
    zip_files = get_zip(folder, file_mask, size_value, size_operator, creation_time_value, creation_time_operator)

    return {"normal_files": normal_files, "zip_files": zip_files}
