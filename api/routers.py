from fastapi import APIRouter

from api.endpoints.search_endpoint import router as search_router
from api.endpoints.health_check import router as health_check_router


router = APIRouter()
router.include_router(search_router)
router.include_router(health_check_router)
