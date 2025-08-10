from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemes.bookings import Booking


class BookingsRepository(BaseRepository):
    model =  BookingsOrm
    schema =  Booking