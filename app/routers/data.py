import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger("app.routers.data")

router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get("/")
async def get_data():
    raise HTTPException(status_code=501, detail="Not Implemented Yet")