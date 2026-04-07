"""Менеджер раскладок Qtile.

Модуль отвечает за:
- получение конфигураций раскладок из `ThemeController`,
- сборку объектов раскладок через `BaseFactory`,
- валидацию входных данных и единое логирование ошибок.
"""

from logging import Logger

from libqtile import layout

from exceptions.layout_exceptions import LayoutConfigurationError, LayoutNotFoundError
from settings.base_factory import BaseFactory
from settings.logger import get_logger
from settings.theme_controller import ThemeController

logger: Logger = get_logger("qtile.layouts", file="logger")


class LayoutsManager:
    """Собирает список раскладок Qtile на основе темы и JSON-конфигураций.

    Args:
        theme_controller: Инициализированный контроллер темы.

    Raises:
        LayoutConfigurationError: При невалидных входных данных или сбое фабрики.
    """

    def __init__(self, theme_controller: ThemeController = None) -> None:
        logger.info("Инициализация LayoutsManager")

        if theme_controller is None:
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="theme_controller",
                reason="ThemeController не должен быть None",
            )

        self.tc: ThemeController = theme_controller
        self.colors = self.tc.get_theme_color()
        self.settings = self.tc.get_theme_settings()

        if not isinstance(self.colors, dict):
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="theme_color",
                reason="Ожидался словарь цветов темы",
            )

        if not isinstance(self.settings, dict):
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="theme_settings",
                reason="Ожидался словарь настроек темы",
            )

        classes = {
            "MonadTall": layout.MonadTall,
            "Max": layout.Max,
            "Columns": layout.Columns,
            "Tile": layout.Tile,
            "Bsp": layout.Bsp,
            "Stack": layout.Stack,
        }
        fallback = [layout.MonadTall(border_width=2), layout.Max()]

        themes = self.tc.get_theme_layouts()
        if not isinstance(themes, list):
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="theme_layouts",
                reason="Ожидался список конфигураций раскладок",
            )

        logger.debug(
            f"Конфигураций раскладок: {len(themes)}, зарегистрировано классов: {len(classes)}"
        )

        try:
            self.factory = BaseFactory(
                themes=themes,
                classes=classes,
                fallback=fallback,
                colors=self.colors,
                settings=self.settings,
            )
            logger.info("Фабрика раскладок успешно создана")
        except Exception as e:
            logger.error(f"Ошибка создания фабрики раскладок: {e}")
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="factory",
                reason=str(e),
            ) from e

    def get_layouts(self) -> list:
        """Возвращает список собранных раскладок Qtile.

        Returns:
            Непустой список объектов раскладок.

        Raises:
            LayoutConfigurationError: При ошибке сборки.
            LayoutNotFoundError: Если после сборки список пуст.
        """
        logger.debug("Сборка раскладок")
        try:
            layouts = self.factory.build()
        except Exception as e:
            logger.error(f"Ошибка сборки раскладок: {e}")
            raise LayoutConfigurationError(
                layout_name="LayoutsManager",
                parameter="build",
                reason=str(e),
            ) from e

        if not layouts:
            logger.error("Список раскладок пуст после сборки")
            raise LayoutNotFoundError(
                layout_name="unknown",
                available_layouts=list(self.factory.classes.keys()),
            )

        logger.info(f"Раскладки успешно собраны: {len(layouts)} шт.")
        return layouts
