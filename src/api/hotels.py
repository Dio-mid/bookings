from fastapi import Query, APIRouter, Body
from src.schemes.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    start_index = (pagination.page - 1) * pagination.per_page
    end_index = start_index + pagination.per_page
    paginated_hotels = hotels_[start_index:end_index]
    return paginated_hotels
    # return hotels_[per_page * (page-1):][:per_page]


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={ #Body(embed=True) для передачи именно JSON и для только одного параметра
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        }
    }
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
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