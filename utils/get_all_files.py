from datetime import datetime
from pathlib import Path
from typing import List

from schemas.search_schema import SearchSettings


def get_all_files(search_settings: SearchSettings, provided_path: str) -> List[Path]:
    """ Get list of all file names in target directory and all subdirectories/zip-archives """
    folder = Path(provided_path)

    good_names = [item for item in folder.rglob(search_settings.file_mask) if item.is_file()]
    good_size = check_size(search_settings.size.value, search_settings.size.operator, good_names)
    good_files = check_creation_time(
        search_settings.creation_time.value,
        search_settings.creation_time.operator,
        good_size
    )

    return good_files


def check_size(value: int, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if the files sizes are allowed """
    op = {"eq": lambda item_size: item_size == value,
          "gt": lambda item_size: item_size > value,
          "lt": lambda item_size: item_size < value,
          "ge": lambda item_size: item_size >= value,
          "le": lambda item_size: item_size <= value,
    }

    good_files = []

    for item in paths:
        if op[operator](item.stat().st_size):
            good_files.append(item)

    return good_files


def check_creation_time(value: datetime, operator: str, paths: List[Path]) -> List[Path]:
    """ Check if a files creation time are allowed """
    op = {"eq": lambda item_creation_time: item_creation_time == value,
          "gt": lambda item_creation_time: item_creation_time > value,
          "lt": lambda item_creation_time: item_creation_time < value,
          "ge": lambda item_creation_time: item_creation_time >= value,
          "le": lambda item_creation_time: item_creation_time <= value,
    }

    good_files = []

    for item in paths:
        creation_time = datetime.fromtimestamp(item.stat().st_ctime)
        if op[operator](creation_time):
            good_files.append(item)

    return good_files
