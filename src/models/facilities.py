import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base

# Для ruff
if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(  # relationship связь
        back_populates="facilities",  # Чтобы Алхимия понимала между чем устанавливается связь, нужно указать название атрибута в другом классе
        secondary="rooms_facilities",  # название таблицы
    )


# m2m таблица
class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
