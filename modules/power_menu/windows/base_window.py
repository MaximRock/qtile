from tkinter import Tk, Toplevel

import customtkinter as ctk
from config_pm.window_config import WindowConfig


class BaseWindow:
    """
    Миксин для управления окном.

    Предоставляет:
        - обработку Escape (закрытие окна)
        - захват и удержание фокуса (topmost + grab)
        - настройку геометрии (размер, ресайз)
    """

    def setup_window(
        self,
        window: Tk | Toplevel | ctk.CTk | ctk.CTkToplevel,
        config: WindowConfig,
    ) -> None:
        """
        Применяет поведение окна.

        Параметры:
            window:
                Экземпляр окна (Tk / Toplevel / CTk).

            config (WindowConfig):
                Конфигурация поведения:
                    - escape: закрытие по Escape
                    - focus: удержание фокуса и topmost

        Поведение:
            - Escape → безопасное закрытие окна
            - Focus → окно всегда поверх и не теряет фокус
        """
        if config.escape:
            window.bind("<Escape>", lambda e: self._safe_destroy(window))

        if config.focus:
            window.attributes("-topmost", True)
            window.focus_force()
            window.grab_set()
            window.bind(
                "<FocusOut>",
                lambda e: window.after(
                    50, lambda: (window.lift(), window.focus_force(), window.grab_set())
                ),
            )

    def _safe_destroy(self, window) -> None:
        """
        Безопасно закрывает окно.

        Перед закрытием:
            - пытается освободить grab (если установлен)

        Игнорирует:
            RuntimeError — если grab не был установлен
        """
        try:
            window.grab_release()
        except RuntimeError:
            ...
        window.destroy()

    def setup_geometry(
        self, window: Tk | Toplevel | ctk.CTk | ctk.CTkToplevel, config: WindowConfig
    ) -> None:
        """
        Применяет геометрию окна.

        Параметры:
            window:
                Экземпляр окна.

            config (WindowConfig):
                Конфигурация:
                    - geometry: строка вида "WIDTHxHEIGHT"
                    - resizable: (bool, bool) — изменение размера

        Применяет:
            - размер окна (geometry)
            - возможность ресайза (resizable)
        """
        if config.geometry:
            window.geometry(config.geometry)

        window.resizable(*config.resizable)
