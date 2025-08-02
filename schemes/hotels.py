from pydantic import BaseModel, Field

# pydentic схема, для соблюдения DRY
class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    title: str | None = Field(None) # так как это схема, а не api ручка, Body [Body(None) был] уже не нужен
    name: str | None = Field(None) # вместо Field(None) можно использовать просто None
