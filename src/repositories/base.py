# Паттерн Репозиторий/DAO (между бизнес-логикой и БД)
# Это паттерн, который позволяет работать с данными так, как будто они рядом с нами (в оперативной памяти)
# Мы работаем с ними как будто они уже есть у нас в приложении, а не мы идем в какую-то БД
# Крайне удобно работать с данными через репозиторий

# Паттерн DataMapper (реализуется через внешний класс) - преобразует из модели Алхимии в Pydentic схему и наоборот
# Отдает на вход бизнес сущности(Pydentic схемы) и возвращает тоже их (а не бд сущности)
# Таким образом слою бизнес-логики без разницы с какими моделями работает репозиторий, как он преобразует данные и т.д.
# DataMapper нужен, для того чтобы изолировать бизнес логику, к которой относятся эндпоинты от логики общения с БД

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None # Каждый репозиторий, который будет наследоваться от BaseRepository, будет иметь свою модель
    schema: BaseModel = None

    def __init__(self, session): # Открываем только одну сессию, чтобы Алхимия не занимала соединения к БД при вызове разных запросов
        self.session = session


    async def get_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        # return result.scalars().all() # Возвращает объект БД
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()] # Возвращает pydentic схему
        # Pydentic умеет работать не только со своими сущностями и словарями, он может доставать атрибуты из ЭкзКлас - from_attributes=True

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        # return result.scalars().one_or_none()
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        #returning чтобы возвращалось то, что было добавлено в БД, можно указывать что конкретно(self.model.id, s.m.title и т.д.)
        result = await self.session.execute(add_stmt)
        # return result.scalars().one()
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel,exclude_unset: bool = False, **filter_by):
        edit_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        # exclude_unset дает возможность исключать поля, которые не были переданы клиентом (для patch ручки)
        await self.session.execute(edit_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)