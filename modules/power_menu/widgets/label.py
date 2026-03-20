import customtkinter as ctk

from .base_widget import BaseWidget


class Label(BaseWidget, ctk.CTkLabel):
    def __init__(self, parent, text: str = "", **kwargs) -> None:
        super().__init__(parent, text=text, **kwargs)
