from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingAddRequest(BaseModel):
    data_from: date
    date_to: date
    price: int

class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    data_from: date
    date_to: date
    price: int

class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
