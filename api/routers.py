from fastapi import APIRouter

from api.endpoints.search_endpoint import router as search_router


router = APIRouter()
router.include_router(search_router)
