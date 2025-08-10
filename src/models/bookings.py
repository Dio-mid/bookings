from datetime import date

from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


# Не забываем импортировать в env.py
class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    data_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property # продвинутый property Алхимии, классная вещь
    def total_price(self):
        return self.price * (self.date_to - self.data_from).days