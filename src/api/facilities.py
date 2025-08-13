from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemes.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facilities(
        db: DBDep,
        facilities_data: FacilitiesAdd
):
    facilities = db.facilities.add(facilities_data)
    await db.commit()

    return {"status": "OK", "data": facilities}