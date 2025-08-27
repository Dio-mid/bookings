from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn


import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent)) # Позволяет определить путь текущего файла через Path(__file__)
# определить его родителя через .parent (src) и его родителя .parent (backend_proj) и добавить ее в пути, с которыми может работать интерпретатор

# Теперь интерпретатор понимает что за src, можно запускать python src/main.py, services.msc для включения БД через командную строку
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()
    # При выключении/перезагрузке приложения


app = FastAPI(lifespan=lifespan)

# Подключаем API
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app")