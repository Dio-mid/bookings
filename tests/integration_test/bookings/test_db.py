from datetime import date

from src.schemes.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        data_from=date(year=2025, month=8, day=10),
        date_to=date(year=2025, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.bookings.get_all()
    await db.bookings.delete()

    await db.commit()
