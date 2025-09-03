from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.schemes.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
