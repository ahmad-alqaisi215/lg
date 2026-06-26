# ./src/core/logger.py

from datetime import datetime
from logging import (DEBUG, FileHandler, Formatter, Logger, StreamHandler,
                     getLogger)
from zoneinfo import ZoneInfo

from src.core.settings import get_settings
from src.core.timezone import ITALY_TZ


class ItalyFormatter(Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=ITALY_TZ)
        return dt.strftime(datefmt or "%Y-%m-%d %H:%M:%S")


def get_logger(name: str) -> Logger:
    logger = getLogger(name)
    s = get_settings()

    if logger.handlers:
        return logger

    formatter = ItalyFormatter(
        fmt="[%(name)s-%(filename)s-%(lineno)s | %(asctime)s | %(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = StreamHandler()
    file_handler = FileHandler(s.LOG_DIR)

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(s.LOG_LEVEL)

    logger.info(f"New `{name}` logger is registered successfully.")

    return logger