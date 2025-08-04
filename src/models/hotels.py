from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

# Для миграций в Python чаще всего используется библиотека Alembic.
# Для того чтобы изменять состояние БД через Python, используется библиотека Alembic, написанная автором Алхимии.
# Миграции позволяют управлять состоянием БД через Python, не прикасаясь к написанию SQL запросов
# Всегда можно откатиться к нужному состоянию БД, быстро и качественно

# alembic init src/migrations , в корне, затем в  конфигурационном файле alembic.ini дописать prepend_sys_path = . src
# alembic revision --autogenerate -m "initial migration" создает миграцию
# чтобы накатить миграции alembic upgrade head, вместо head на работе указывают ревизию  057f9f1c534c из файла миграций

# Таблица/модель БД
class HotelsOrm(Base):
    # название таблицы
    __tablename__ = "hotels"

    # столбцы
    id: Mapped[int] = mapped_column(primary_key=True) # Первичный ключ, обозначат, что столбец уникальный
    title: Mapped[str] = mapped_column(String(length=100)) # mapped_column для определения свойств столбца, если нужно
    location: Mapped[str]