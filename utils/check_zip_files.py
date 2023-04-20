from pathlib import Path
from typing import List
from datetime import datetime
from zipfile import ZipFile
import os
import re


def get_archives(folder: Path) -> List[str]:
    """ Get all paths to zip-archives without sub-archives """
    archives = []
    folder_path = str(folder.absolute())
    for item in os.listdir(folder_path):
        if item.endswith(".zip"):
            archives.append("\\".join([folder_path, item]))

    return archives


def get_files_from_archive(archive: str, file_mask: str, size_value: int, size_operator: str, creation_time_value: datetime, creation_time_operator: str) -> List[str]:
    """ Get zip-archive and check every file to conditions """
    size_compare = {
        "eq": lambda item_size: item_size == size_value,
        "gt": lambda item_size: item_size > size_value,
        "lt": lambda item_size: item_size < size_value,
        "ge": lambda item_size: item_size >= size_value,
        "le": lambda item_size: item_size <= size_value,
	}

    time_compare = {
        "eq": lambda item_creation_time: item_creation_time == creation_time_value,
        "gt": lambda item_creation_time: item_creation_time > creation_time_value,
        "lt": lambda item_creation_time: item_creation_time < creation_time_value,
        "ge": lambda item_creation_time: item_creation_time >= creation_time_value,
        "le": lambda item_creation_time: item_creation_time <= creation_time_value,
    }


    regex_pattern = file_mask.replace(".", r"\.").replace("*", r".*")

    paths = []
    with ZipFile(archive, "r") as arc:
        for path in arc.namelist():
            conditions = (
                not path.endswith("/"),
                not path.endswith(".zip"),
                re.match(regex_pattern, path.split("/")[-1]),
                size_compare[size_operator](arc.getinfo(path).file_size),
                time_compare[creation_time_operator](datetime(*arc.getinfo(path).date_time)),
            )
            if all(conditions):
                paths.append(path)

    return paths


def get_zip(folder: Path, file_mask, size_value, size_operator, creation_time_value, creation_time_operator) -> dict[str, list[str]]:
    """ Get dictionary {"path_to_archive": [good_file1_in_archive, good_file2_in_archive]} """
    archives = get_archives(folder=folder)
    result = {}
    for archive in archives:
        result[archive] = get_files_from_archive(
            archive, file_mask, size_value, size_operator, creation_time_value, creation_time_operator
		)

    return result
