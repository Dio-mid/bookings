from fastapi import FastAPI
import uvicorn


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent)) # Позволяет определить путь текущего файла через Path(__file__)
# определить его родителя через .parent (src) и его родителя .parent (backend_proj) и добавить ее в пути, с которыми может работать интерпретатор

# Теперь интерпретатор понимает что за src, можно запускать python src/main.py
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels) # Подключаем API
app.include_router(router_rooms)
app.include_router(router_bookings)


if __name__ == "__main__":
    uvicorn.run("main:app")