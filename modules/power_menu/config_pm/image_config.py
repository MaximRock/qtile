from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .exceptions import ImageConfigError


@dataclass(slots=True)
class ImageConfig:
    path: Path
    size: tuple[int, int] = (40, 40)


PATH_DIR_ICONS: str = "modules/power_menu/icons"


def get_icon(path_getter: Callable[[str], Path], name: str) -> ImageConfig:
    """Получить конфиг иконки по имени"""

    if not callable(path_getter):
        raise ImageConfigError("path_getter должен быть callable")

    if not name or not isinstance(name, str):
        raise ImageConfigError("name должен быть непустой строкой")

    try:
        path: Path = path_getter(f"{PATH_DIR_ICONS}/{name}.png")
    except Exception as e:
        raise ImageConfigError("Ошибка получения пути к иконке") from e

    if not isinstance(path, Path):
        raise ImageConfigError("path_getter должен возвращать pathlib.Path")

    if not path.exists():
        raise ImageConfigError(f"Иконка не найдена: {path}")

    return ImageConfig(path=path)
