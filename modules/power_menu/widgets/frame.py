import customtkinter as ctk

from .base_widget import BaseWidget


class Frame(BaseWidget, ctk.CTkFrame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
