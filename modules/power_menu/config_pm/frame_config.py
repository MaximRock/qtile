from dataclasses import dataclass

from .exceptions import ConfigError, FrameConfigError

DEFAULT_CONFIG_FRAME: dict[str, str | int | tuple] = {
    "fg_color": "transparent",
    "height": 60,
    "column": 0,
    "columnspan": 2,
    "padx": (10, 0),
}


@dataclass(slots=True)
class FrameConfig:
    """
    Конфигурация фрейма для построения UI (например, в Tkinter/CustomTkinter).

    Атрибуты:
        fg_color (str):
            Цвет фона фрейма.

        height (int):
            Высота фрейма.

        row (int):
            Позиция строки в grid layout.

        column (int):
            Позиция колонки в grid layout.

        columnspan (int):
            Сколько колонок занимает фрейм.

        sticky (str):
            Поведение растяжения в grid (например: "n", "s", "e", "w", "nsew").

        pady (tuple[int, int] | int):
            Внешние отступы по вертикали.

        padx (tuple[int, int] | int):
            Внешние отступы по горизонтали.
    """
    fg_color: str
    height: int
    row: int
    column: int
    columnspan: int
    sticky: str
    pady: tuple[int, int] | int
    padx: tuple[int, int] | int


def create_frame_config(
    row: int,
    sticky: str = "ew",
    pady: tuple[int, int] | int = (0, 0),
    **kwargs,
) -> FrameConfig:
    """
    Фабрика для создания конфигурации фрейма с валидацией и значениями по умолчанию.

    Позволяет централизованно управлять настройками layout и предотвращает
    некорректные конфигурации.

    Args:
        row (int):
            Номер строки в grid layout (обязательный параметр).

        sticky (str, optional):
            Поведение растяжения фрейма в grid.
            По умолчанию "ew".

        pady (tuple[int, int] | int, optional):
            Отступы по вертикали.
            Может быть int или кортеж (top, bottom).
            По умолчанию (0, 0).

        **kwargs:
            Дополнительные параметры (зарезервированы).
            Попытка переопределить поля FrameConfig приведёт к ошибке.

    Raises:
        FrameConfigError:
            Если переданы некорректные типы аргументов.

        ConfigError:
            Если происходит конфликт полей или ошибка при создании конфигурации.

    Returns:
        FrameConfig:
            Готовый объект конфигурации фрейма.

    Пример:
        >>> config = create_frame_config(row=1, sticky="nsew", pady=10)
    """
    if not isinstance(row, int):
        raise FrameConfigError("row должен быть int")

    if not isinstance(sticky, str):
        raise FrameConfigError("sticky должен быть str")

    if not isinstance(pady, (tuple, int)):
        raise FrameConfigError("pady должен быть tuple или int")

    reserved: set[str] = set(FrameConfig.__dataclass_fields__.keys())
    conflict: set[str] = reserved.intersection(kwargs)
    if conflict:
        raise ConfigError(f"Нельзя переопределять поля: {conflict}")

    try:
        return FrameConfig(
            fg_color=DEFAULT_CONFIG_FRAME["fg_color"],
            height=DEFAULT_CONFIG_FRAME["height"],
            column=DEFAULT_CONFIG_FRAME["column"],
            columnspan=DEFAULT_CONFIG_FRAME["columnspan"],
            padx=DEFAULT_CONFIG_FRAME["padx"],
            row=row,
            sticky=sticky,
            pady=pady,
            **kwargs,
        )
    except Exception as e:
        raise ConfigError("Ошибка конфигурации frame") from e


HEADER_FRAME: FrameConfig = create_frame_config(
    row=0,
    sticky="ew",
    pady=(10, 0),
)

BUTTON_FRAME: FrameConfig = create_frame_config(
    row=1,
    sticky="nsew",
    pady=10,
)
