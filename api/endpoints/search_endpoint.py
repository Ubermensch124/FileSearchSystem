import os

from fastapi import APIRouter
from pydantic import UUID4

from config import settings
from schemas import SearchSettings, SearchId, SearchResult


router = APIRouter(tags=["main"], prefix="")


@router.post("/search", response_model=SearchId)
def search_settings(search_config: SearchSettings):
    return {f"Objects at {settings.TARGET_DIRECTORY}": os.listdir(settings.TARGET_DIRECTORY)}


@router.get("/searches/{search_id}", response_model=SearchResult)
def search_result(search_id: UUID4):
    return {f"Objects at {settings.TARGET_DIRECTORY}": os.listdir(settings.TARGET_DIRECTORY)}
