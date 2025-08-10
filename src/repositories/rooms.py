from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemes.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room