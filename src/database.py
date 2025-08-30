from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

# ORM — object-relational mapping или объектно-реляционное отображение — это способ взаимодействия приложения с базой данных
# посредством синтаксиса языка, на котором написано приложение. (Для Python самая популярная - SQLAlchemy)
# SQLAlchemy сама не отправляет запросы в БД, для этих целей она использует уже готовые библиотеки, называемые драйверами,
# например, psycopg2 или asyncpg(спасает сильно от SQL-инъекций). SQLAlchemy дает возможность формировать как сырые SQL запросы, так и писать через ORM.


engine = create_async_engine(settings.DB_URL) # Подключение к БД
# echo=True - На каждый запрос, который Алхимия будет посылать в БД, мы будем видеть в консоли этот SQL-запрос
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool) # Возможно только одно соединение (способ работы с Алхимией для Celery и Pytest)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False) # Фабрика сессий
# Новый объект сессии, который по сути является новой транзакцией (из SQL) в БД
# В этой сессии мы можем вставить в одну таблицу, убрать из другой, счетчик добавить, сделать выборку (SELECT) и т.д.
# В самом конце мы завершаем транзакцию и добавляем ее в БД, если что-то пойдет не так в процессе, то все просто откатится назад
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

class Base(DeclarativeBase):# Нужен, чтоб наследовать от него все модели в проекте
    # В атрибуте metadata будут накапливаться данные о всех таблицах, столбцах и т.д.
    pass