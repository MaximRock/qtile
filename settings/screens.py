"""Менеджер экранов Qtile.

Модуль загружает конфигурацию экрана из JSON, валидирует параметры,
создаёт объект(ы) `libqtile.config.Screen` и предоставляет их наружу.

Ошибки конфигурации и создания экрана поднимаются через специализированные
исключения из `exceptions/screen_exceptions.py`.
"""

import json
from logging import Logger
from pathlib import Path

from libqtile.config import Screen

from exceptions.screen_exceptions import (
    BarConfigurationError,
    ScreenConfigurationError,
    ScreenNotFoundError,
)
from settings.bar import BarManager
from settings.logger import get_logger
from settings.path import QtilePath
from settings.theme_controller import ThemeController

logger: Logger = get_logger("qtile.screens", file="logger")


class ScreenManager:
    """Менеджер экранов для Qtile.

    Класс читает конфигурацию из `config_qtile/settings_json/screen.json`,
    объединяет её с базовыми настройками темы и создаёт список экранов.

    Args:
        theme_controller: Инициализированный `ThemeController`.
        config_file: Имя JSON-файла конфигурации экрана.
        walls_dir: Директория с обоями относительно корня Qtile-конфига.

    Raises:
        ScreenConfigurationError: При невалидной конфигурации экрана.
        BarConfigurationError: При ошибке инициализации верхней панели.
    """

    def __init__(
        self,
        theme_controller: ThemeController,
        config_file: str = "screen.json",
        walls_dir: str = "walls",
    ) -> None:
        if theme_controller is None:
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="theme_controller",
                reason="ThemeController не должен быть None",
            )

        if not isinstance(config_file, str) or not config_file.strip():
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="config_file",
                reason="Имя файла конфигурации должно быть непустой строкой",
            )

        if not isinstance(walls_dir, str) or not walls_dir.strip():
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="walls_dir",
                reason="Путь к директории обоев должен быть непустой строкой",
            )

        self.tc: ThemeController = theme_controller
        self.config_file: str = config_file.strip()
        self.walls_dir: str = walls_dir.strip()
        self.qp: QtilePath = QtilePath()

        self.settings: dict = self.tc.get_theme_settings()
        if not isinstance(self.settings, dict):
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="theme_settings",
                reason="Ожидался словарь настроек темы",
            )

        self._config: dict = {}
        self._screens: list[Screen] = []

        logger.info(
            "Инициализация ScreenManager: "
            f"config_file={self.config_file}, walls_dir={self.walls_dir}"
        )

        self._load_config()
        self._create_screens()

    def _load_config(self) -> None:
        """Загружает JSON-конфигурацию экрана в `self._config`.

        Raises:
            ScreenConfigurationError: Если файл отсутствует, JSON невалиден
                или корень JSON не является объектом.
        """
        config_path: Path = self.qp.get(
            f"config_qtile/settings_json/{self.config_file}"
        )

        try:
            with open(config_path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            logger.error(f"Файл конфигурации экранов не найден: {config_path}")
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="config_file",
                reason=f"Файл не найден: {config_path}",
            ) from e
        except json.JSONDecodeError as e:
            logger.error(f"Некорректный JSON в {config_path}: {e}")
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="config_file",
                reason=f"Некорректный JSON: {e}",
            ) from e
        except OSError as e:
            logger.error(f"Ошибка чтения файла {config_path}: {e}")
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="config_file",
                reason=str(e),
            ) from e

        if not isinstance(data, dict):
            raise ScreenConfigurationError(
                screen_id="default",
                parameter="config_file",
                reason="Корень JSON должен быть объектом",
            )

        self._config = data
        logger.info(f"Загружен конфиг экранов: {config_path}")

    def _resolve_wallpaper(self) -> Path:
        """Формирует и валидирует путь к файлу обоев.

        Returns:
            Полный путь к существующему файлу обоев.

        Raises:
            ScreenConfigurationError: Если параметры обоев невалидны
                или итоговый файл не существует.
        """
        wallpaper_name = self._config.get(
            "wallpaper", self.settings.get("wallpaper", "vodoem")
        )
        wallpaper_ext = self._config.get(
            "wallpaper_ext", self.settings.get("wallpaper_ext", ".jpeg")
        )

        if not isinstance(wallpaper_name, str) or not wallpaper_name.strip():
            raise ScreenConfigurationError(
                screen_id=0,
                parameter="wallpaper",
                reason="Имя обоев должно быть непустой строкой",
            )

        if not isinstance(wallpaper_ext, str) or not wallpaper_ext.strip():
            raise ScreenConfigurationError(
                screen_id=0,
                parameter="wallpaper_ext",
                reason="Расширение обоев должно быть непустой строкой",
            )

        wallpaper_name = wallpaper_name.strip()
        wallpaper_ext = wallpaper_ext.strip()

        if not wallpaper_ext.startswith("."):
            wallpaper_ext = f".{wallpaper_ext}"

        wallpaper_path: Path = self.qp.get(
            f"{self.walls_dir}/{wallpaper_name}{wallpaper_ext}"
        )

        if not wallpaper_path.exists() or not wallpaper_path.is_file():
            raise ScreenConfigurationError(
                screen_id=0,
                parameter="wallpaper",
                reason=f"Файл обоев не найден: {wallpaper_path}",
            )

        return wallpaper_path

    def _resolve_wallpaper_mode(self) -> str:
        """Возвращает и валидирует режим отображения обоев.

        Raises:
            ScreenConfigurationError: Если режим задан некорректно.
        """
        wallpaper_mode = self._config.get(
            "wallpaper_mode", self.settings.get("wallpaper_mode", "center")
        )

        if not isinstance(wallpaper_mode, str) or not wallpaper_mode.strip():
            raise ScreenConfigurationError(
                screen_id=0,
                parameter="wallpaper_mode",
                reason="Режим обоев должен быть непустой строкой",
            )

        return wallpaper_mode.strip()

    def _create_screens(self) -> None:
        """Создаёт список экранов `self._screens`.

        Raises:
            BarConfigurationError: Если не удалось инициализировать панель.
            ScreenConfigurationError: Если параметры экрана невалидны.
        """
        try:
            bar_manager: BarManager = BarManager(theme_controller=self.tc)
            top_bar = bar_manager.init_bar()
        except Exception as e:
            logger.error(f"Ошибка инициализации панели: {e}")
            raise BarConfigurationError(
                screen_id=0,
                position="top",
                reason=str(e),
            ) from e

        if top_bar is None:
            raise BarConfigurationError(
                screen_id=0,
                position="top",
                reason="init_bar вернул None",
            )

        wallpaper_path = self._resolve_wallpaper()
        wallpaper_mode = self._resolve_wallpaper_mode()

        try:
            self._screens = [
                Screen(
                    top=top_bar,
                    wallpaper=str(wallpaper_path),
                    wallpaper_mode=wallpaper_mode,
                )
            ]
        except Exception as e:
            logger.error(f"Ошибка создания объекта Screen: {e}")
            raise ScreenConfigurationError(
                screen_id=0,
                parameter="screen",
                reason=str(e),
            ) from e

        logger.info(
            "Экран успешно создан: "
            f"wallpaper={wallpaper_path.name}, mode={wallpaper_mode}"
        )

    def get_screens(self) -> list[Screen]:
        """Возвращает текущий список экранов.

        Raises:
            ScreenNotFoundError: Если список экранов пуст.
        """
        if not self._screens:
            logger.error("Список экранов пуст")
            raise ScreenNotFoundError(screen_id="default", available_screens=[])

        return self._screens

    def get_config(self) -> dict:
        """Возвращает загруженную конфигурацию экрана."""
        return self._config

    def reload(self) -> None:
        """Перезагружает конфигурацию и пересоздаёт экраны."""
        logger.info("Перезагрузка ScreenManager")
        self._load_config()
        self._create_screens()
        logger.info("ScreenManager успешно перезагружен")
