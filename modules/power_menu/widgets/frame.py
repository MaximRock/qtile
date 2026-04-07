import customtkinter as ctk
from config_pm.exceptions import FrameWidgetsError

from .base_widget import BaseWidget


class Frame(BaseWidget, ctk.CTkFrame):
    """
    Контейнер (Frame) для группировки виджетов в Power Menu.

    Наследует:
        BaseWidget: базовый функционал
        ctk.CTkFrame: контейнер из CustomTkinter

    Аргументы:
        parent: родительский контейнер (обязательный)
        **kwargs: параметры CTkFrame (fg_color, corner_radius и т.д.)
    """

    def __init__(self, parent, **kwargs) -> None:
        """Инициализация Frame с базовыми проверками."""

        if parent is None:
            raise FrameWidgetsError("Frame: 'parent' не может быть None")

        if "master" in kwargs:
            raise FrameWidgetsError("Frame: используйте 'parent', а не 'master'")

        allowed_kwargs = {
            "width",
            "height",
            "corner_radius",
            "border_width",
            "fg_color",
            "border_color",
            "background_corner_colors",
        }

        unknown_keys: set[str] = set(kwargs) - allowed_kwargs
        if unknown_keys:
            raise FrameWidgetsError(
                f"Frame: неподдерживаемые параметры: {', '.join(unknown_keys)}"
            )

        if "width" in kwargs and (
            not isinstance(kwargs["width"], int) or kwargs["width"] <= 0
        ):
            raise FrameWidgetsError("Frame: width должен быть положительным int")

        if "height" in kwargs and (
            not isinstance(kwargs["height"], int) or kwargs["height"] <= 0
        ):
            raise FrameWidgetsError("Frame: height должен быть положительным int")

        super().__init__(parent, **kwargs)
