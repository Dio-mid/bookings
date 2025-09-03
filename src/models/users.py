from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=200), unique=True
    )  # Запрещает добавлять если email уже есть
    hashed_password: Mapped[str] = mapped_column(String(length=200))
