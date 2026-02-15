from settings.path import QtilePath
import subprocess
from pathlib import Path


class Autostart:
    """Класс для управления автозапуском скриптов."""

    def __init__(self, script_name: str = "autostart.sh"):
        """
        Инициализация с именем скрипта.

        Args:
            script_name: Имя скрипта автозапуска
        """
        self.qp = QtilePath()
        self.script = self.qp.get(script_name)

    def run(self) -> None:
        """Запустить скрипт автозапуска."""
        if self.script.exists():
            subprocess.run([str(self.script)])

    def get_path(self) -> Path:
        """Получить путь к скрипту."""
        return self.script
