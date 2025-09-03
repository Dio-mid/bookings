from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemes.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])  # для main.py

# Паттерн Use Case (в DDD) - это часть бизнес-логики приложения, которая определяет конкретный сценарий использования (для реализации коротких ручек)


@router.get("")
@cache(expire=20)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    data_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        data_from,
        date_to,
    )
    # return await db.hotels.get_filtered_by_time(
    #     data_from=data_from,
    #     date_to=date_to,
    #     location=location,
    #     title=title,
    #     limit=pagination.per_page,
    #     offset=pagination.per_page * (pagination.page - 1),
    # )

    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=pagination.per_page,
    #     offset=pagination.per_page * (pagination.page-1)
    # ) # Вместо кода ниже

    # async with async_session_maker() as session:
    #     return await HotelsRepository(session).get_all(
    #         location=location,
    #         title=title,
    #         limit=pagination.per_page,
    #         offset=pagination.per_page * (pagination.page-1)
    #     ) # Вместо кода ниже

    # # per_page = pagination.per_page or 5 Если нет дефолтного значения
    # async with async_session_maker() as session:
    #     # Запрос на выборку данных - query, запросы на изменение - stmt
    #     query = select(HotelsOrm)
    #     # Фильтрация, func - дает возможность использовать все функции из БД
    #     if location:
    #         # query = query.filter_by(location=location)
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower())) # Фильтрация по подстроке
    #         # contains() == like(f"%{}%"))
    #     if title:
    #         query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
    #
    #     query = (
    #         query
    #         .limit(pagination.per_page)
    #         .offset(pagination.per_page * (pagination.page-1)) # limit и offset это SQL слова для пагинации
    #     )
    #
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #
    #     result = await session.execute(query) # Все что с await - это отправка запросов в БД, возвращает в result итератор
    #
    #     hotels = result.scalars().all() # hotels - список, без scalars в списке будут кортежи в консоли
    #     # commit() Не нужен так как select запрос, мы ничего не меняем
    #     return hotels
    #
    #     # return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.get("/{hotel_id}")
async def get_one_hotel(hotel_id: int, db: DBDep):
    return await HotelService(db).get_hotel(hotel_id)


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={  # Body(embed=True) для передачи именно JSON и для только одного параметра
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Deluxe 5 звезд у моря",
                    "location": "Сочи, улица Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Luxe У фонтана",
                    "location": "Дубай, улица Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}

    # hotel = await db.hotels.add(hotel_data)
    # await db.commit()

    # async with async_session_maker() as session:
    #     hotel = await HotelsRepository(session).add(hotel_data)
    #     await session.commit() # нужно указывать здесь, а не в репозитории, чтобы находиться внутри одной транзакции на один пользовательский запрос
    #     # Комиты нужно делать в самом конце, когда со всеми данными были произведены изменения
    # return {"status": "OK", "data": hotel}

    # async with async_session_maker() as session: # Как только он закроется, сессия (какое-то подключение к БД) тоже закроется
    #     # Этот АсинКонМен нужен, чтобы заблокировать/захватить одно из соединений Алхимии
    #
    #     # Делаем запрос на вставку в таблицу, через model_dump преобразуем pydentic схему к словарю и распаковываем **
    #     add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
    #
    #     # Для дебага, увидим в консоли, какой SQL-запрос отправит Алхимия в БД
    #     print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
    #
    #     await session.execute(add_hotel_stmt) # Отправляем запрос в БД, Алхимия его переводит на чистый/сырой SQL
    #     await session.commit() # Обязательна эта строка, чтоб добавлялось в БД, т.к. в DBeaver и других под капотом
    #     # отправляется запрос с start transaction - запрос - commit
    #
    # return {"status": "OK"} # Принято в RestAPI возвращать JSON формат, а не строку


@router.put("/{hotel_id}")
async def put_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="<h1>Тут мы частично обновляем данные об отеле: можно title и/или location</h1>",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}