from collections.abc import Callable
from dataclasses import dataclass

import customtkinter as ctk

from .exceptions import ButtonConfigError, ConfigError, ThemeError


@dataclass
class ButtonConfig:
    """
    Конфигурация кнопки для UI (CustomTkinter).

    Атрибуты:
        text (str):
            Текст кнопки.

        command (Callable | None):
            Функция, вызываемая при нажатии.

        compound (str | None):
            Расположение текста относительно изображения ("top", "left" и т.д.).

        image (ctk.CTkImage | None):
            Иконка кнопки.

        bind_key (str | None):
            Горячая клавиша для активации кнопки.

        fg_color (str | None):
            Основной цвет кнопки.

        hover_color (str | None):
            Цвет при наведении.

        text_color (str | None):
            Цвет текста.

        font (tuple[str, int]):
            Шрифт (имя, размер).

        width (int):
            Ширина кнопки.

        height (int):
            Высота кнопки.
        border_width (int):
            Толщина рамки.

        border_color (str | None):
            Цвет рамки.

        corner_radius (int):
            Радиус скругления.

        row (int):
            Позиция строки в grid.

        column (int):
            Позиция колонки в grid.

        padx (tuple[int, int] | int):
            Отступы по горизонтали.

        pady (tuple[int, int] | int):
            Отступы по вертикали.
    """
    text: str = ""
    command: Callable | None = None
    compound: str | None = "top"
    image: ctk.CTkImage | None = None
    bind_key: str | None = None
    fg_color: str | None = None
    hover_color: str | None = None
    text_color: str | None = None
    font: tuple[str, int] = ("Jetbrains Mono", 24)
    width: int = 150
    height: int = 160
    border_width: int = 2
    border_color: str | None = None
    corner_radius: int = 2
    row: int = 0
    column: int = 0
    padx: tuple[int, int] | int = (5, 2)
    pady: tuple[int, int] | int = 10


def create_button_config(
    theme: dict,
    text: str,
    command: Callable,
    bind_key: str,
    image: ctk.CTkImage | None,
    column: int,
    border_color: str,
    **kwargs,
) -> ButtonConfig:
    """
    Фабрика для создания конфигурации кнопки с валидацией и автоматическим
    применением цветов из темы.

    Args:
        theme (dict):
            Словарь темы с цветами.
            Ожидается структура:
            {
                "background": {"surface0": str, "surface1": str},
                "text": {"primary": str}
            }

        text (str):
            Текст кнопки (обязательный параметр).

        command (Callable):
            Функция, вызываемая при нажатии (обязательный параметр).

        bind_key (str):
            Горячая клавиша (обязательный параметр).

        image (ctk.CTkImage | None):
            Иконка кнопки.

        column (int):
            Позиция колонки в grid layout.

        border_color (str):
            Цвет рамки кнопки (обязательный параметр).

        **kwargs:
            Дополнительные параметры (зарезервированы).
            Попытка переопределить поля ButtonConfig приведёт к ошибке.

                Raises:
        ThemeError:
            Если theme отсутствует, имеет неверный формат или не содержит нужных ключей.

        ButtonConfigError:
            Если обязательные параметры отсутствуют или имеют неверный тип.

        ConfigError:
            Если возникает конфликт полей или ошибка при создании конфигурации.

    Returns:
        ButtonConfig:
            Готовый объект конфигурации кнопки.

    Пример:
        >>> config = create_button_config(
        ...     theme=theme,
        ...     text="Lock",
        ...     command=lock_screen,
        ...     bind_key="l",
        ...     image=icon,
        ...     column=0,
        ...     border_color="#ffffff"
        ... )
    """

    if theme is None:
        raise ThemeError("theme обязателен")

    if not isinstance(theme, dict) or not theme:
        raise ThemeError("theme должен быть непустым словарём")

    if not text:
        raise ButtonConfigError("text обязателен")

    if not callable(command):
        raise ButtonConfigError("command должен быть callable")

    if image is not None and not isinstance(image, ctk.CTkImage):
        raise ButtonConfigError("image должен быть PIL.Image или None")

    if not bind_key:
        raise ButtonConfigError("bind_key обязателен")

    if not isinstance(column, int):
        raise ButtonConfigError("column должен быть int")

    if border_color is None:
        raise ButtonConfigError("border_color обязателен")

    reserved: set[str] = {
        "text",
        "command",
        "compound",
        "image",
        "bind_key",
        "fg_color",
        "hover_color",
        "text_color",
        "font",
        "width",
        "height",
        "border_width",
        "border_color",
        "corner_radius",
        "row",
        "column",
        "padx",
        "pady",
    }

    conflict: set[str] = set(kwargs) & reserved
    if conflict:
        raise ConfigError(f"Нельзя переопределять поля: {conflict}")

    try:
        fg_color = theme["background"]["surface0"]
        hover_color = theme["background"]["surface1"]
        text_color = theme["text"]["primary"]
    except KeyError as e:
        raise ThemeError(f"Нет ключа {e}") from e

    try:
        config = ButtonConfig(
            text=text,
            command=command,
            image=image,
            bind_key=bind_key,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            border_color=border_color,
            column=column,
            **kwargs,
        )
    except Exception as e:
        raise ConfigError("Ошибка конфигурации кнопки") from e
    return config
