from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Указываем имя переменной, которая есть в .env
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # Формат DSN
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env") # extra="ignore" не выдаст ошибку если количество переменных в .env не совпадает с атрибутами Settings

settings = Settings()

#                                             Переменные окружения (файл .env)
#
# (. перед началом файла означает, что файл скрытый и по умолчанию его не видно в обычном проводнике
# (нужна либо комбинация клавиш, либо вызывать контекстное меню))
# Эти файлы никогда не пушатся в github/lab (нужно передать в gitignore)
#
# Здесь находятся любые чувствительные данные (пароли, логины, хосты, порты, подключения, api-ключи и т.д.)