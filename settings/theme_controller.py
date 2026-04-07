"""Контроллер тем Qtile.

Модуль отвечает за загрузку и валидацию:
- базовых настроек темы (`base.json`),
- компонентных конфигураций (`layouts.json`, `widgets.json`, `bar.json`),
- цветового пресета активной темы (`theme/presets/<theme>.json`).

При ошибках загрузки/структуры выбрасываются специализированные исключения
из `exceptions/theme_exceptions.py`.
"""

import json
from logging import Logger
from pathlib import Path
from typing import Any

from config_qtile.theme.theme_model import Theme
from constants import SETTINGS_JSON_PATH, THEME_PRESETS_PATH
from exceptions.theme_exceptions import (
    ThemeLoadError,
    ThemeNotFoundError,
    ThemeValidationError,
)
from settings.logger import get_logger
from settings.path import QtilePath

logger: Logger = get_logger("qtile.theme", file="logger")


class ThemeController:
    """Загружает и предоставляет данные темы для остальных менеджеров конфигурации.

    Args:
        theme_color: Имя цветового пресета (например, `tokyonight`, `gruvbox`).

    Raises:
        ThemeValidationError: Если входные данные или структура JSON невалидны.
        ThemeLoadError: Если файл невозможно прочитать/распарсить.
        ThemeNotFoundError: Если запрошенный пресет темы отсутствует.
    """

    def __init__(self, theme_color: str) -> None:
        if not isinstance(theme_color, str) or not theme_color.strip():
            raise ThemeValidationError(
                theme_name="unknown",
                field="theme_color",
                reason="Имя темы должно быть непустой строкой",
            )

        self.theme_name_color: str = theme_color.strip()
        logger.info(f"Инициализация ThemeController с темой: {self.theme_name_color}")

        self.qp = QtilePath()
        # "config_qtile/settings_json"
        self.theme_path: Path = self.qp.get(SETTINGS_JSON_PATH)
        # "config_qtile/theme/presets"
        self.theme_color_path: Path = self.qp.get(THEME_PRESETS_PATH)

        self.theme_name_layouts = "layouts"
        self.theme_name_widgets = "widgets"
        self.theme_name_bar = "bar"

        self.theme_settings: dict = self._load_theme_settings()
        self.theme_layouts: list[Theme] = self._load_theme_layouts()
        self.theme_widgets: list[Theme] = self._load_theme_widgets()
        self.theme_bar: list[Theme] = self._load_theme_bar()
        self.theme_color: dict = self._load_theme_color()

    def _read_json(self, file_path: Path, theme_name: str) -> Any:
        """Читает JSON-файл и преобразует ошибки чтения в `ThemeLoadError`.

        Args:
            file_path: Абсолютный/резолвленный путь к JSON-файлу.
            theme_name: Логическое имя темы/конфига для текста исключения.

        Returns:
            Данные, полученные из `json.load`.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            logger.error(f"Файл темы не найден: {file_path}")
            raise ThemeLoadError(theme_name, str(file_path), str(e)) from e
        except json.JSONDecodeError as e:
            logger.error(f"Некорректный JSON в файле темы: {file_path}")
            raise ThemeLoadError(
                theme_name, str(file_path), f"Некорректный JSON: {e}"
            ) from e
        except OSError as e:
            logger.error(f"Ошибка чтения файла темы: {file_path} | {e}")
            raise ThemeLoadError(theme_name, str(file_path), str(e)) from e

    def _load_theme_settings(self) -> dict:
        """Загружает и валидирует общие настройки темы из `base.json`."""
        theme_name = "base"
        theme_file: Path = self.theme_path / "base.json"
        data = self._read_json(theme_file, theme_name)

        if not isinstance(data, dict):
            raise ThemeValidationError(
                theme_name=theme_name,
                field="root",
                reason="Ожидался JSON-объект (dict)",
            )

        logger.info(f"Загружены базовые настройки темы: {theme_file}")
        return data

    def _load(self, theme_name: str) -> list[Theme]:
        """Загружает и валидирует компонентный JSON-файл в список `Theme`.

        Ожидаемый формат файла: массив объектов вида
        `{"name": "...", "config": {...}}`.
        """
        theme_file: Path = self.theme_path / f"{theme_name}.json"
        data = self._read_json(theme_file, theme_name)

        if not isinstance(data, list):
            raise ThemeValidationError(
                theme_name=theme_name,
                field="root",
                reason="Ожидался JSON-массив (list)",
            )

        themes: list[Theme] = []
        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ThemeValidationError(
                    theme_name=theme_name,
                    field=f"[{index}]",
                    reason="Элемент должен быть объектом",
                )

            item_name = item.get("name", "")
            if not isinstance(item_name, str) or not item_name.strip():
                raise ThemeValidationError(
                    theme_name=theme_name,
                    field=f"[{index}].name",
                    reason="Поле 'name' должно быть непустой строкой",
                )

            item_config = item.get("config", {})
            if not isinstance(item_config, dict):
                raise ThemeValidationError(
                    theme_name=theme_name,
                    field=f"[{index}].config",
                    reason="Поле 'config' должно быть объектом",
                )

            themes.append(Theme(name=item_name.strip(), config=item_config))

        logger.info(f"Загружен файл темы '{theme_name}.json': {len(themes)} элементов")
        return themes

    def _load_theme_layouts(self) -> list[Theme]:
        """Возвращает конфигурацию раскладок (`layouts.json`)."""
        return self._load(self.theme_name_layouts)

    def _load_theme_widgets(self) -> list[Theme]:
        """Возвращает конфигурацию виджетов (`widgets.json`)."""
        return self._load(self.theme_name_widgets)

    def _load_theme_bar(self) -> list[Theme]:
        """Возвращает конфигурацию панели (`bar.json`)."""
        return self._load(self.theme_name_bar)

    def _get_available_themes(self) -> list[str]:
        """Собирает список доступных файлов-пресетов темы без расширения."""
        if not self.theme_color_path.exists() or not self.theme_color_path.is_dir():
            return []

        return sorted(
            [
                file.stem
                for file in self.theme_color_path.glob("*.json")
                if file.is_file()
            ]
        )

    def _load_theme_color(self) -> dict:
        """Загружает цветовой пресет выбранной темы и валидирует структуру."""
        theme_file: Path = self.theme_color_path / f"{self.theme_name_color}.json"

        if not theme_file.exists():
            available_themes = self._get_available_themes()
            logger.error(
                f"Запрошенная тема '{self.theme_name_color}' не найдена. "
                f"Доступно: "
                f"{', '.join(available_themes) if available_themes else 'пусто'}"
            )
            raise ThemeNotFoundError(
                theme_name=self.theme_name_color,
                available_themes=available_themes,
            )

        data = self._read_json(theme_file, self.theme_name_color)

        if not isinstance(data, list) or not data:
            raise ThemeValidationError(
                theme_name=self.theme_name_color,
                field="root",
                reason="Ожидался непустой JSON-массив (list)",
            )

        first_item = data[0]
        if not isinstance(first_item, dict):
            raise ThemeValidationError(
                theme_name=self.theme_name_color,
                field="[0]",
                reason="Первый элемент должен быть объектом",
            )

        config = first_item.get("config")
        if not isinstance(config, dict):
            raise ThemeValidationError(
                theme_name=self.theme_name_color,
                field="[0].config",
                reason="Поле 'config' должно быть объектом",
            )

        logger.info(f"Загружена цветовая тема: {theme_file}")
        return config

    def get_theme_settings(self) -> dict:
        """Возвращает словарь базовых настроек темы из `base.json`."""
        return self.theme_settings

    def get_theme_layouts(self) -> list[Theme]:
        """Возвращает список конфигураций раскладок."""
        return self.theme_layouts

    def get_theme_widgets(self) -> list[Theme]:
        """Возвращает список конфигураций виджетов."""
        return self.theme_widgets

    def get_theme_bar(self) -> list[Theme]:
        """Возвращает список конфигураций панели."""
        return self.theme_bar

    def get_theme_color(self) -> dict:
        """Возвращает словарь цветовых переменных активного пресета."""
        return self.theme_color
