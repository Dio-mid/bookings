from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository
from src.repositories.bookings import BookingsRepository


# Реализация асинхронного контекстного менеджера
# async with async_session_maker() as session:
class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)

        return self # as session:

    async def __aexit__(self, *args):
        # КонтМен делает откат изменений в случае возникновения ошибки во время соединения с БД/отправления транзакции, взаимодействия с ней и тд
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()