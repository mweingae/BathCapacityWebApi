import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger("app.routers.settings")

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)

@router.get("/")
async def get_settings():
    raise HTTPException(status_code=501, detail="Not Implemented Yet")

@router.patch("/")
async def update_settings():
    raise HTTPException(status_code=501, detail="Not Implemented Yet")