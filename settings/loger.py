import logging
from pathlib import Path
from settings.path import QtilePath

qp = QtilePath()

LOG_DIR: Path = qp.get("log")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILES = {
    "mouse": LOG_DIR / "mouse.log",
    "basefactory": LOG_DIR / "basefactory.log",
    "default": LOG_DIR / "loger.log",
    "qtile_startup": LOG_DIR / "qtile_startup.log",
}


def get_logger(name: str, file: str | None = None) -> logging.Logger:
    """
    Возвращает файловый логгер.
    По умолчанию файл выбирается через LOG_FILES или default.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_file = (
            LOG_FILES.get(file, LOG_FILES["default"]) if file else LOG_FILES["default"]
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
