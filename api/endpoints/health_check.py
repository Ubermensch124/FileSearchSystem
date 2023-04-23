from fastapi import APIRouter


router = APIRouter(tags=["Misc"], prefix="/api")

@router.get("/ping")
def health_check():
    return {"Result": "pong"}
