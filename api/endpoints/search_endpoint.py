import os

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from config import settings
from schemas.search_schema import SearchSettings, SearchId, SearchResult
from db.connection import get_session
from db.repositories.search_db import add_search_to_db, get_search_from_db


router = APIRouter(tags=["main"], prefix="")


@router.post("/search", response_model=SearchId)
def search_settings(search_config: SearchSettings, session: Session = Depends(get_session)):
    search_id = add_search_to_db(search_config=search_config, session=session)
    return {"search_id": search_id}


# response_model=SearchResult
@router.get("/searches/{search_id}")
def search_result(search_id: UUID4, session: Session = Depends(get_session)):
    search_config = get_search_from_db(search_id=search_id, session=session)
    return SearchSettings.from_orm(search_config)
