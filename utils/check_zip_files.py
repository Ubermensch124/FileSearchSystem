from pathlib import Path
from typing import List
from datetime import datetime
from zipfile import ZipFile
import os
import re

from utils.compare import compare_dict
from schemas.search_schema import SearchSettings


def get_archives(folder: Path) -> List[str]:
    """ Get all paths to zip-archives without sub-archives """
    archives = []
    folder_path = str(folder.absolute())
    for item in os.listdir(folder_path):
        if item.endswith(".zip"):
            archives.append("\\".join([folder_path, item]))

    return archives


def get_files_from_archive(archive: str, search_settings: SearchSettings) -> List[str]:
    """ Get zip-archive and check every file to conditions """
    regex_pattern = search_settings.file_mask.replace(".", r"\.").replace("*", r".*")
    
    size_operator = search_settings.size.operator
    size_value = search_settings.size.value
    creation_time_operator = search_settings.creation_time.operator
    creation_time_value = search_settings.creation_time.value.isoformat()

    paths = []
    with ZipFile(archive, "r") as arc:
        for path in arc.namelist():
            conditions = (
                not path.endswith("/"),
                not path.endswith(".zip"),
                re.match(regex_pattern, path.split("/")[-1]),
                compare_dict[size_operator](arc.getinfo(path).file_size, size_value),
                compare_dict[creation_time_operator](datetime(*arc.getinfo(path).date_time).replace(microsecond=0).isoformat(), creation_time_value),
            )
            if all(conditions):
                paths.append(path)

    return paths


def get_zip(folder: Path, search_settings: SearchSettings) -> dict[str, list[str]]:
    """ Get dictionary {"path_to_archive": [good_file1_in_archive, good_file2_in_archive]} """
    archives = get_archives(folder=folder)
    result = {}
    for archive in archives:
        result[archive] = get_files_from_archive(archive, search_settings)

    return result
