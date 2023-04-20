from pathlib import Path
from typing import List
from datetime import datetime


def check_names_normal(folder: Path, file_mask: str) -> List[Path]:
    """ Check if the files have allowed names """
    good_paths = []
    for item in folder.rglob(file_mask):
        if item.is_file() and item.suffix != ".zip":
            good_paths.append(item)

    return good_paths


def check_size_normal(value: int, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if the files sizes are allowed """
    size_compare = {
        "eq": lambda item_size: item_size == value,
        "gt": lambda item_size: item_size > value,
        "lt": lambda item_size: item_size < value,
        "ge": lambda item_size: item_size >= value,
        "le": lambda item_size: item_size <= value,
    }

    good_paths = []

    for item in paths:
        if size_compare[operator](item.stat().st_size):
            good_paths.append(item)

    return good_paths


def check_creation_time_normal(value: datetime, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if a files creation time are allowed """
    time_compare = {
        "eq": lambda item_creation_time: item_creation_time == value,
        "gt": lambda item_creation_time: item_creation_time > value,
        "lt": lambda item_creation_time: item_creation_time < value,
        "ge": lambda item_creation_time: item_creation_time >= value,
        "le": lambda item_creation_time: item_creation_time <= value,
    }

    good_paths = []

    for item in paths:
        creation_time = datetime.fromtimestamp(item.stat().st_ctime)
        if time_compare[operator](creation_time):
            good_paths.append(item)

    return good_paths


def get_normal(folder: Path, file_mask, size_value, size_operator, creation_time_value, creation_time_operator) -> List[Path]:
    """ Get all good files from directories and subdirectories """
    good_names = check_names_normal(folder, file_mask)
    good_size = check_size_normal(size_value, size_operator, good_names)
    good_files = check_creation_time_normal(creation_time_value, creation_time_operator, good_size)

    return good_files
