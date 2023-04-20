from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from config import settings
from schemas.search_schema import SearchSettings, SearchId, SearchResult
from db.connection import get_session
from db.repositories.search_db import add_search_to_db, get_search_from_db
from service.extract_text import check_text_from_files, celery_app
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


router = APIRouter(tags=["main"], prefix="")


@router.post("/search", response_model=SearchId)
def search_settings(search_config: SearchSettings, session: Session = Depends(get_session)):
    search_id = add_search_to_db(search_config=search_config, session=session)
    return {"search_id": search_id}


@router.get("/searches/{search_id}", response_model=SearchResult, response_model_exclude_none=True)
def search_result(search_id: UUID4, session: Session = Depends(get_session)):
    task_in_queue = redis_client.exists(str(search_id))
    if task_in_queue:
        print('Oieiei')
        return {"finished": False}
    
    task = AsyncResult(str(search_id), app=celery_app)
    if task.status == "SUCCESS":
        return task.result
    print(task.status)
    search_config = get_search_from_db(search_id=search_id, session=session)
    search_config = SearchSettings.from_orm(search_config)
    
    task = check_text_from_files.apply_async(args=[search_config.json(), settings.TARGET_DIRECTORY], task_id=str(search_id))
    return {"finished": False}
