import enum
from functools import lru_cache
from typing import Optional
from pydantic import AnyUrl, BaseSettings


class Backend(enum.Enum):
    INMEMORY = "InMemory"
    SQLITE = "SQLite"


class Settings(BaseSettings):
    backend: Backend = Backend.INMEMORY
    backend_db_url: Optional[str] = "sqlite:///.db/data.db"


@lru_cache()
def get_settings():
    return Settings()
