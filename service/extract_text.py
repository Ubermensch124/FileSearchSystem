import json
from zipfile import ZipFile

import tika
tika.initVM()
from tika import parser
from celery import Celery

from schemas.search_schema import SearchSettings
from service.get_all_files import get_all_files


celery_app = Celery(
    'tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)

@celery_app.task
def check_text_from_files(search_settings: str, target_directory: str):
    """ Search text_template in files and return paths """    
    json_settings = json.loads(search_settings)
    search_settings = SearchSettings(**json_settings)

    file_paths = get_all_files(search_settings, target_directory)
    normal_files = file_paths["normal_files"]
    zip_dict = file_paths["zip_files"]
    search_string = search_settings.text

    # просматриваем файлы из обычных директорий
    paths = []
    for path in normal_files:
        path = str(path.absolute())
        parsed = parser.from_file(path)["content"]
        if search_string is None or search_string == "":
            paths.append(path)
        elif parsed is not None and parsed.find(search_string) > -1:
            paths.append(path)

    # просматриваем файлы из zip-архивов первого слоя
    for archive_path, archive_files in zip_dict.items():
        with ZipFile(archive_path) as arc:
            for path in archive_files:
                with arc.open(path) as file:
                    parsed = parser.from_file(file)["content"]
                    if search_string is None or search_string == "":
                        paths.append(archive_path + "\\" + path.replace("/", "\\"))
                    elif parsed is not None and parsed.find(search_string) > -1:
                        paths.append(archive_path + "\\" + path.replace("/", "\\"))

    return {"finished": True, "paths": paths}
