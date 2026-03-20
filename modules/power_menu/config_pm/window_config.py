from dataclasses import dataclass

from .exceptions import ConfigError, WindowConfigError


@dataclass(slots=True)
class WindowConfig:
    """
    Конфигурация окна приложения.

    Атрибуты:
        geometry (str):
            Размер окна в формате "WIDTHxHEIGHT" (например "600x250").

        resizable (tuple[bool, bool]):
            Возможность изменения размера окна (width, height).

        escape (bool):
            Закрытие окна по клавише Escape.

        focus (bool):
            Захват фокуса (topmost + grab_set + возврат фокуса).
    """

    geometry: str
    resizable: tuple[bool, bool]
    escape: bool
    focus: bool

    def __post_init__(self) -> None:
        """Валидация конфигурации окна"""

        # geometry
        if not isinstance(self.geometry, str) or not self.geometry:
            raise WindowConfigError("geometry должен быть непустой строкой")

        # проверка формата "600x250"
        if "x" not in self.geometry:
            raise WindowConfigError('geometry должен быть в формате "WIDTHxHEIGHT"')

        # resizable
        try:
            w, h = self.resizable
            if not isinstance(w, bool) or not isinstance(h, bool):
                raise ConfigError
        except Exception as e:
            raise WindowConfigError("resizable должен быть tuple[bool, bool]") from e

        # escape
        if not isinstance(self.escape, bool):
            raise WindowConfigError("escape должен быть bool")

        # focus
        if not isinstance(self.focus, bool):
            raise WindowConfigError("focus должен быть bool")


POWER_MENU_WINDOW = WindowConfig(
    geometry="600x250",
    resizable=(False, False),
    escape=True,
    focus=True,
)
