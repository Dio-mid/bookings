from datetime import date


from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemes.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            data_from: date,
            date_to: date
    ):
        """
        with rooms_count as (
	        select room_id, count(*) as rooms_booked from bookings
	        where data_from <= '2025-11-07' and date_to >= '2025-07-01'
	        group by room_id
        ),
        rooms_left_table as (
	        select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
	        from rooms
	        left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        """

        rooms_ids_to_get = rooms_ids_for_booking(data_from, date_to, hotel_id)

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get)) # Номера доступные для бронирования
