from fastapi import Query, APIRouter, Body

from src.database import async_session_maker, engine
from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.schemes.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"]) # для main.py


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля")
):
    # per_page = pagination.per_page or 5 Если нет дефолтного значения
    async with async_session_maker() as session:
        # Запрос на выборку данных - query, запросы на изменение - stmt
        query = select(HotelsOrm)
        # Фильтрация
        if location:
            query = query.filter_by(location=location)
        if title:
            query = query.filter_by(title=title)

        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page-1)) # limit и offset это SQL слова для пагинации
        )

        result = await session.execute(query) # Все что с await - это отправка запросов в БД, возвращает в result итератор

        hotels = result.scalars().all() # hotels - список, без scalars в списке будут кортежи в консоли
        # commit() Не нужен так как select запрос, мы ничего не меняем
        return hotels

        # return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={ #Body(embed=True) для передачи именно JSON и для только одного параметра
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Отель Deluxe 5 звезд у моря",
            "location": "Сочи, улица Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Luxe У фонтана",
            "location": "Дубай, улица Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session: # Как только он закроется, сессия (какое-то подключение к БД) тоже закроется
        # Этот АсинКонМен нужен, чтобы заблокировать/захватить одно из соединений Алхимии

        # Делаем запрос на вставку в таблицу, через model_dump преобразуем pydentic схему к словарю и распаковываем **
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump()) # stmt для всего кроме get api

        # Для дебага, чтобы видеть, что запрос компилируется в то, во что ожидали
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        # Увидим в консоли, какой SQL-запрос отправит Алхимия в БД

        await session.execute(add_hotel_stmt) # Отправляем запрос в БД, Алхимия его переводит на чистый/сырой SQL
        await session.commit() # Обязательна эта строка, чтоб добавлялось в БД, т.к. в DBeaver и других под капотом
        # отправляется запрос с start transaction - запрос - commit

    return {"status": "OK"} # Принято в RestAPI возвращать JSON формат, а не строку


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"} # Принято в RestAPI возвращать JSON формат, а не строку


@router.put("/{hotel_id}")
def put_hotels(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных",
           description="<h1>Тут мы частично обновляем данные об отеле: можно title и/или name</h1>")
def patch_hotel(hotel_id: int,
               hotel_data: HotelPatch):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id and hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel["id"] == hotel_id and hotel_data.name:
            hotel["name"] = hotel_data.name

    return {"status": "OK"}