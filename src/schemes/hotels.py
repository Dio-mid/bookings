from pydantic import BaseModel, Field

# pydentic схема, для соблюдения DRY
class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

class HotelPatch(BaseModel):
    title: str | None = Field(None) # так как это схема, а не api ручка, Body [Body(None) был] уже не нужен
    location: str | None = Field(None) # вместо Field(None) можно использовать просто None
