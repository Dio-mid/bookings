#Паттерн Репозиторий/DAO (между бизнес-логикой и БД)
# Это паттерн, который позволяет работать с данными так, как будто они рядом с нами (в оперативной памяти)
# Мы работаем с ними как будто они уже есть у нас в приложении, а не мы идем в какую-то БД
# Крайне удобно работать с данными через репозиторий

from sqlalchemy import select, insert


class BaseRepository:
    model = None # Каждый репозиторий, который будет наследоваться от BaseRepository, будет иметь свою модель

    def __init__(self, session): # Открываем только одну сессию, чтобы Алхимия не занимала соединения к БД при вызове разных запросов
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add_values(self, **kwargs):
        add_stmt = insert(self.model).values(**kwargs)
        await self.session.execute(add_stmt)
