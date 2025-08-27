from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemes.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=20) # кэширует в браузере и на бэкенд запрос не отправляется (Cache-Control в F12), если не тот браузер у клиента или еще что-то, то тогда пойдет в Redis запрос
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
    # Реализация кэширования с экспирацией без декоратора
    # facilities_from_cache = await redis_manager.get("facilities")
    # if not facilities_from_cache:
    #     print("ИДУ В БАЗУ ДАННЫХ")
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json, 20)
    #
    #     return facilities
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts


@router.post("")
async def add_facilities(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}