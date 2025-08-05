from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, insert, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()


    async def add_values(self, **kwargs):
            add_stmt = insert(HotelsOrm).values(**kwargs.model_dump())
            print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            hotel = await self.session.execute(add_stmt)
            return {"status": "OK", "data": hotel}