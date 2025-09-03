from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(data_from: date, date_to: date, hotel_id: int | None = None):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(  # В filter_by нельзя делать проверки на >, <, in и тд
            BookingsOrm.data_from <= date_to,
            BookingsOrm.date_to >= data_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")  # Чтобы преобразовалось ровно в таком же виде как сырой запрос
    )

    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            # так как это CTE, а не модель Алхимии, к колонке нужно обращаться через .c.название_колонки
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    rooms_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")  # Подзапрос
    )

    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(select(rooms_ids_for_hotel)),
            # select id from rooms where hotel_id = hotel_id
        )
    )

    # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
    # return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))  # Номера доступные для бронирования

    return rooms_ids_to_get
