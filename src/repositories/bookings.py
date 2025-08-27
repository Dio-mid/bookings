from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemes.bookings import Booking


class BookingsRepository(BaseRepository):
    model =  BookingsOrm
    # schema =  Booking
    mapper = BookingDataMapper