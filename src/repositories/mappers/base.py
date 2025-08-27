# Паттерн DataMapper позволяет связать модель и схему без их взаимозависимости,
# То есть модель не привязана к схеме, а схема - к модели

from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    # Превращает sql alchemy модель в pydentic схему
    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    # Принимаем pydentic схему - возвращаем модель алхимии
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
