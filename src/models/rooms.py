from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

# Rooms - сущности завязанные на Hotels
class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    # Если мы хотим связать две таблицы нам нужен внешний ключ. Так как комната привязана к отелю
    # она ссылается на какой-то отель, поэтому параметр именуем hotel_id (название сущности и id)
    # Внешний ключ - ForeignKey, в нем указываем: первое - название(__tablename__) таблицы и название столбца (id)
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]