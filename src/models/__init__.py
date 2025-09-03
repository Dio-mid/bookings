from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.models.bookings import BookingsOrm
from src.models.facilities import (
    FacilitiesOrm,
)  # Нужно импортировать сам файл, чтобы alembic увидел, не нужно импорт две модели

# Для ruff
__all__ = [
    "HotelsOrm",
    "RoomsOrm",
    "UsersOrm",
    "BookingsOrm",
    "FacilitiesOrm",
]
