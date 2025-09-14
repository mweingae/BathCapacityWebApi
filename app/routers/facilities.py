import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger("app.routers.facilities")

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"]
)

@router.get("/")
async def get_facilities():
    raise HTTPException(status_code=501, detail="Not Implemented Yet")

@router.get("/{facility_id}")
async def get_facility(facility_id : int):
    raise HTTPException(status_code=501, detail="Not Implemented Yet")

@router.post("/")
async def create_facility():
    raise HTTPException(status_code=501, detail="Not Implemented Yet")

@router.patch("/{facility_id}")
async def update_facility(facility_id : int):
    raise HTTPException(status_code=501, detail="Not Implemented Yet")

@router.delete("/{facility_id}")
async def delete_facility(facility_id : int):
    raise HTTPException(status_code=501, detail="Not Implemented Yet")