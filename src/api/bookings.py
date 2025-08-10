from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemes.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.post("/{room_id}/bookings")
async def create_room(room_id: int, db: DBDep, booking_data: BookingAddRequest = Body()):
    _booking_data = BookingAdd(room_id=room_id, **booking_data.model_dump())
    booking = db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}