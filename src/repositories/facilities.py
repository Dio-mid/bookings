from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemes.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model =  FacilitiesOrm
    schema =  Facilities