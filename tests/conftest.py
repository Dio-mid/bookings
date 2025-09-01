import json
from unittest import mock

# Мок - заменяет на время теста запрос во внешний сервис (Redis, RabbitMQ и тд) на пустышку
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start() # Мокает запрос к Redis
# Первым параметром указываем, что меняем (декоратор @cache), а вторым, на что (пустой декоратор в виде лямбды)


import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.schemes.hotels import HotelAdd
from src.schemes.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


# # Для локальной разработки, это позволит тестам работать без Redis
# @pytest.fixture(autouse=True, scope="session")
# def init_cache():
#     FastAPICache.init(InMemoryBackend(), prefix="test-cache")


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db

# Перезаписывание зависимости
app.dependency_overrides[get_db] = get_db_null_pool # Везде, где используется get_db, т.е. где в апишке идет подключение к БД, будет использоваться null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):

    # Для создания тестовой БД на основе тех БД, что уже есть
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )

@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac