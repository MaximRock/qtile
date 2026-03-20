import subprocess
from tkinter import Tk, Toplevel

import customtkinter as ctk
from config_pm.exceptions import ButtonWidgetsError

from .base_widget import BaseWidget


class Button(BaseWidget, ctk.CTkButton):
    """
    Кнопка для Power Menu в Qtile с привязкой к горячим клавишам и встроенными
    действиями: блокировка экрана, перезагрузка, выключение, выход из сессии.

    Наследует:
        BaseWidget: базовые функции виджетов
        ctk.CTkButton: стилизованная кнопка CustomTkinter

    Аргументы:
        parent (Tk | Toplevel): родительское окно
        text (str): текст кнопки
        command (Callable, optional): функция, вызываемая при нажатии кнопки
        bind_key (str, optional): клавиша для привязки к кнопке (например, "<Escape>")
        **kwargs: дополнительные параметры для CTkButton
    """
    def __init__(
        self, parent, text: str = "", command=None, bind_key=None, **kwargs
    ) -> None:
        """Инициализация кнопки с возможностью привязки горячей клавиши."""
        super().__init__(parent, text=text, command=command, **kwargs)

        if bind_key:
            self.bind_key(bind_key)

    def bind_key(self, key: str) -> None:
        """
        Привязка клавиши к вызову кнопки.

        Аргументы:
            key (str): клавиша в формате Tkinter (например, "<Return>", "<Escape>")
        """
        root: Tk | Toplevel = self.winfo_toplevel()
        root.bind(key, lambda event: self.invoke())

    def _run_command(self, command: list[str], wait: bool = False) -> None:
        """
        Выполняет системную команду через subprocess.

        Аргументы:
            command (list[str]):
                список аргументов команды (например, ["systemctl", "reboot"])
            wait (bool): если True, команда запускается асинхронно через Popen,
                            и после этого приложение закрывается
                         если False, команда выполняется синхронно через run()
        """
        if wait:
            subprocess.Popen(command, start_new_session=True)
            self.quit_app()
        else:
            subprocess.run(command, check=True)

    def lock(self) -> None:
        """
        Заблокировать экран с помощью xlock и закрыть Power Menu.

        Исключения:
            ButtonWidgetsError: если не удалось выполнить команду
        """
        try:
            self._run_command(
                command=["xlock", "-mode", "matrix", "-delay", "50000"], wait=True
            )
        except Exception as e:
            raise ButtonWidgetsError(f"Ошибка при запуске xlock: {e}") from e

    def reboot(self) -> None:
        """
        Выключить систему.

        Исключения:
            ButtonWidgetsError: если не удалось выполнить команду
        """
        try:
            self._run_command(["systemctl", "reboot"], wait=False)
        except Exception as e:
            raise ButtonWidgetsError(f"Ошибка выполнения команды: {e}") from e

    def poweroff(self) -> None:
        """
        Выключить систему.

        Исключения:
            ButtonWidgetsError: если не удалось выполнить команду
        """
        try:
            self._run_command(["systemctl", "poweroff"], wait=False)
        except Exception as e:
            raise ButtonWidgetsError(f"Ошибка выполнения команды: {e}") from e

    def logout(self) -> None:
        """
        Выйти из текущей сессии Qtile.

        Исключения:
            ButtonWidgetsError: если не удалось выполнить команду
        """
        try:
            self._run_command(
                ["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"], wait=True
            )
        except Exception as e:
            raise ButtonWidgetsError(f"Ошибка выполнения команды: {e}") from e

    def quit_app(self) -> None:
        """
        Закрыть Power Menu, завершив работу окна Tk/Toplevel.
        """
        root: Tk | Toplevel = self.winfo_toplevel()
        root.quit()
        root.destroy()
