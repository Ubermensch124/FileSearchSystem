# import os

# import requests

from schemas.search_schema import SearchSettings
from utils.get_all_files import get_all_files

import tika
tika.initVM()
from tika import parser


def check_text_from_files(search_settings: SearchSettings, target_directory: str):
    paths = []
    file_paths = get_all_files(search_settings, target_directory)
    # tika_url = f"http://tika-server:9998/tika"
    # headers = {"Accept": "text/plain"}
    search_string = search_settings.text

    for path in file_paths:
        # with open("path/to/your/file", "rb") as f:
        #     file_data = f.read()
        # response = requests.put(tika_url, data=path, headers=headers)
        path = str(path.absolute())
        parsed = parser.from_file(path)["content"]
        if parsed is not None and parsed.find(search_string) > -1:
            paths.append(path)

    return {"finished": True, "paths": paths}
