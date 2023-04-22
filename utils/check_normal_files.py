from pathlib import Path
from typing import List
from datetime import datetime

from utils.compare import compare_dict


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
        creation_time = datetime.fromtimestamp(item.stat().st_ctime)
        if compare_dict[operator](creation_time, value):
            good_paths.append(item)

    return good_paths


def get_normal(folder: Path, file_mask, size_value, size_operator, creation_time_value, creation_time_operator) -> List[Path]:
    """ Get all good files from directories and subdirectories """
    good_names = check_names_normal(folder, file_mask)
    good_size = check_size_normal(size_value, size_operator, good_names)
    good_files = check_creation_time_normal(creation_time_value, creation_time_operator, good_size)

    return good_files
