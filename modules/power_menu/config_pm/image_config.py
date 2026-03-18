from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageConfig:
    path: Path
    size: tuple[int, int] = (40, 40)


PATH_DIR_ICONS: str = "modules/power_menu/icons"


def get_icon(path_getter: Callable[[str], Path], name: str) -> ImageConfig:
    return ImageConfig(path=path_getter(f"{PATH_DIR_ICONS}/{name}.png"))
