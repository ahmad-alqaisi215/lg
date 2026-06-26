# src/core/settings.py

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from src.core.enums import Category
from typing import ClassVar

ROOT_DIR: Path = Path(__file__)

def _find_root():
    global ROOT_DIR
    ROOT = Path("/")

    while not (ROOT_DIR / "main.py").exists():
        ROOT_DIR = ROOT_DIR.parent

        if ROOT_DIR == ROOT:
            raise FileNotFoundError("Could not find project root dir.")


_find_root()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # LOGS Config
    LOG_DIR: Path = ROOT_DIR / "app.log"
    LOG_LEVEL: str = "DEBUG"

    # Data Config
    DATA_DIR: ClassVar[Path] = ROOT_DIR / "data"
    DATA_RAW_DIR: ClassVar[Path] = DATA_DIR / "raw"
    DATA_RAW_DIR: ClassVar[Path] = DATA_DIR / "processed"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
