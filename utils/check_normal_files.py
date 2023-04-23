from pathlib import Path
from typing import List
from datetime import datetime

from utils.compare import compare_dict
from schemas.search_schema import SearchSettings


def check_names_normal(folder: Path, file_mask: str) -> List[Path]:
    """ Check if the files have allowed names """
    good_paths = []
    for item in folder.rglob(file_mask):
        if item.is_file() and item.suffix != ".zip":
            good_paths.append(item)

    return good_paths


def check_size_normal(value: int, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if the files sizes are allowed """
    good_paths = []

    for item in paths:
        if compare_dict[operator](item.stat().st_size, value):
            good_paths.append(item)

    return good_paths


def check_creation_time_normal(value: datetime, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if a files creation time are allowed """
    good_paths = []

    for item in paths:
        creation_time = datetime.fromtimestamp(item.stat().st_ctime).replace(microsecond=0).isoformat()
        if compare_dict[operator](creation_time, value.isoformat()):
            good_paths.append(item)

    return good_paths


def get_normal(folder: Path, search_settings: SearchSettings) -> List[Path]:
    """ Get all good files from directories and subdirectories """
    good_names = check_names_normal(folder, search_settings.file_mask)
    good_size = check_size_normal(
        search_settings.size.value,
        search_settings.size.operator,
        good_names
    )
    good_files = check_creation_time_normal(
        search_settings.creation_time.value,
        search_settings.creation_time.operator,
        good_size
    )

    return good_files
