import customtkinter as ctk
from config_pm.exceptions import LabelWidgetsError

from .base_widget import BaseWidget


class Label(BaseWidget, ctk.CTkLabel):
    """
    Текстовый виджет (Label) для Power Menu.

    Наследует:
        BaseWidget: базовый функционал
        ctk.CTkLabel: виджет текста из CustomTkinter

    Аргументы:
        parent: родительский контейнер (обязательный)
        text (str): текст для отображения
        **kwargs: дополнительные параметры CTkLabel
    """

    def __init__(self, parent, text: str = "", **kwargs) -> None:
        """
        Инициализация Label с базовыми проверками.
        """

        if parent is None:
            raise LabelWidgetsError("Label: 'parent' не может быть None")

        if not isinstance(text, str):
            raise LabelWidgetsError(
                f"Label: 'text' должен быть строкой, получено {type(text).__name__}"
            )

        text = text.strip()
        if "text" in kwargs:
            raise LabelWidgetsError("Label: 'text' нельзя передавать через kwargs")

        super().__init__(parent, text=text, **kwargs)
