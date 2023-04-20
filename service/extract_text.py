import json

import tika
tika.initVM()
from tika import parser
from celery import Celery

from schemas.search_schema import SearchSettings
from utils.get_all_files import get_all_files


celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1', task_track_started=True)
# celery_app.conf.task_track_started = True

@celery_app.task()
def check_text_from_files(search_settings: str, target_directory: str):
    """ Search text_template in files and return paths """
    # self.update_state(state="PROGRESS")
    
    json_settings = json.loads(search_settings)
    search_settings = SearchSettings(**json_settings)
    
    file_paths = get_all_files(search_settings, target_directory)
    search_string = search_settings.text
    
    paths = []
    for path in file_paths:
        path = str(path.absolute())
        parsed = parser.from_file(path)["content"]
        if parsed is not None and parsed.find(search_string) > -1:
            paths.append(path)

    return {"finished": True, "paths": paths}
