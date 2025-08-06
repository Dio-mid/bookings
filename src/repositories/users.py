from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemes.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User # Именно эту pydentic схему будем передавать в БД