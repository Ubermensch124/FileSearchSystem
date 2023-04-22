from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from celery.result import AsyncResult
import redis

from config import settings
from schemas.search_schema import SearchSettings, SearchId, SearchResult
from db.connection import get_session
from db.repositories.search_db import add_search_to_db, get_search_from_db
from service.extract_text import check_text_from_files, celery_app

router = APIRouter(tags=["main"], prefix="")
redis_store_pending = redis.Redis(host='localhost', port=6379, db=2)


@router.post("/search", response_model=SearchId)
def search_settings(search_config: SearchSettings, session: Session = Depends(get_session)):
    """ Save settings for search and return unique SEARCH_ID """
    search_id = add_search_to_db(search_config=search_config, session=session)
    return {"search_id": search_id}


@router.get("/searches/{search_id}", response_model=SearchResult, response_model_exclude_none=True)
def search_result(search_id: UUID4, session: Session = Depends(get_session)):
    """ Search settings for your SEARCH_ID and return paths to files """    
    task = AsyncResult(str(search_id), app=celery_app)
    if task.status == "SUCCESS":
        redis_store_pending.delete(str(search_id))
        return task.result

    in_redis = redis_store_pending.get(str(search_id))
    if not in_redis or task.status == "FAILURE":
        search_config = get_search_from_db(search_id=search_id, session=session)
        if search_config is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID doesn't exist")
        search_config = SearchSettings.from_orm(search_config)

        task = check_text_from_files.apply_async(
            args=[search_config.json(),
            settings.TARGET_DIRECTORY],
            task_id=str(search_id),
        )
        redis_store_pending.set(str(search_id), "True")

    return {"finished": False}


@router.get("/ping")
def health_check():
    return {"Result": "pong"}
