import subprocess
from tkinter import Tk, Toplevel

import customtkinter as ctk

from .base_widget import BaseWidget


class Button(BaseWidget, ctk.CTkButton):
    def __init__(
        self, parent, text: str = "", command=None, bind_key=None, **kwargs
    ) -> None:
        super().__init__(parent, text=text, command=command, **kwargs)

        if bind_key:
            self.bind_key(bind_key)

    def bind_key(self, key: str) -> None:
        root: Tk | Toplevel = self.winfo_toplevel()
        root.bind(key, lambda event: self.invoke())

    def _run_command(self, command: list[str], wait: bool = False) -> None:
        if wait:
            subprocess.Popen(command, start_new_session=True)
            self.quit_app()
        else:
            subprocess.run(command, check=True)

    def lock(self) -> None:
        """Заблокировать экран и закрыть приложение"""
        try:
            self._run_command(
                command=["xlock", "-mode", "matrix", "-delay", "50000"], wait=True
            )
        except Exception as e:
            print(f"Ошибка при запуске xlock: {e}")

    def reboot(self):
        try:
            self._run_command(["systemctl", "reboot"], wait=False)
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")

    def poweroff(self):
        try:
            self._run_command(["systemctl", "poweroff"], wait=False)
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")

    def logout(self):
        try:
            self._run_command(
                ["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"], wait=True
            )
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")

    def quit_app(self) -> None:
        """Закрыть приложение"""
        root: Tk | Toplevel = self.winfo_toplevel()
        root.quit()
        root.destroy()
