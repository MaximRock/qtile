from tkinter import Tk, Toplevel

import customtkinter as ctk


class BaseWindow:
    """Миксин: Escape + постоянный фокус"""

    def setup_window(
        self,
        window: Tk | Toplevel | ctk.CTk | ctk.CTkToplevel,
        escape: bool = True,
        focus: bool = True,
    ) -> None:
        """Настройка окна: Escape и/или фокус"""
        if escape:
            window.bind("<Escape>", lambda e: self._safe_destroy(window))

        if focus:
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
        """Закрыть с освобождением захвата"""
        try:
            window.grab_release()
        except Exception:
            pass
        window.destroy()
