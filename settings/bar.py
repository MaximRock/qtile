"""Управление панелями (bar) в Qtile.

Модуль предоставляет класс `BarManager`, который:
- инициализирует `ThemeController` и `WidgetManager`;
- создаёт объект `libqtile.bar.Bar` с подставленными настройками.

При ошибках используются исключения из `exceptions/bar_exception.py`.
"""

from logging import Logger
from typing import Any

from libqtile import bar

from exceptions.bar_exception import (
    BarConfigurationError,
    BarInitializationError,
)
from settings.base_factory import BaseFactory
from settings.logger import get_logger
from settings.theme_controller import ThemeController
from settings.widgets import WidgetManager

logger: Logger = get_logger("qtile.bar", file="logger")


class BarManager:
    """Менеджер панелей для Qtile.

    Args:
        theme_controller: Экземпляр ThemeController. Если None, создаётся новый.
    """

    def __init__(self, theme_controller: ThemeController = None) -> None:
        if theme_controller is None:
            logger.warning("BarManager: theme_controller не передан, создаётся новый")
            self.tc = ThemeController()
        else:
            self.tc = theme_controller

        try:
            self.colors = self.tc.get_theme_color()
            self.settings = self.tc.get_theme_settings()

            if not isinstance(self.colors, dict):
                logger.error(
                    f"BarManager: get_theme_color() должен возвращать dict, "
                    f"получено {type(self.colors).__name__}"
                )
                raise BarConfigurationError(
                    bar_id="default",
                    parameter="theme_color",
                    reason="Ожидался словарь цветов",
                )

            if not isinstance(self.settings, dict):
                logger.error(
                    f"BarManager: get_theme_settings() должен возвращать dict, "
                    f"получено {type(self.settings).__name__}"
                )
                raise BarConfigurationError(
                    bar_id="default",
                    parameter="theme_settings",
                    reason="Ожидался словарь настроек",
                )

            logger.debug(
                f"BarManager: загружено {len(self.colors)} цветов, "
                f"{len(self.settings)} настроек"
            )
        except Exception as e:
            logger.error(f"BarManager: ошибка получения настроек темы: {e}")
            raise BarConfigurationError(
                bar_id="default",
                parameter="theme",
                reason=str(e),
            ) from e

        try:
            widget_manager = WidgetManager(theme_controller=self.tc)
            self.widgets = widget_manager.get_widget()

            if not isinstance(self.widgets, list):
                logger.error(
                    f"BarManager: get_widget() должен возвращать list, "
                    f"получено {type(self.widgets).__name__}"
                )
                raise BarConfigurationError(
                    bar_id="default",
                    parameter="widgets",
                    reason="Ожидался список виджетов",
                )

            logger.debug(f"BarManager: создано виджетов: {len(self.widgets)}")
        except Exception as e:
            logger.error(f"BarManager: ошибка создания виджетов: {e}")
            raise BarInitializationError(
                bar_id="default",
                reason=str(e),
            ) from e

        self.factory = BaseFactory(
            themes=self.tc.get_theme_bar(),
            classes={},
            fallback=[],
            colors=self.colors,
            settings=self.settings,
        )

        logger.info("BarManager инициализирован")

    def _validate_bar_config(self, config: dict[str, Any]) -> None:
        """Валидирует конфигурацию панели перед созданием bar.Bar."""
        if not isinstance(config, dict):
            logger.error(
                f"BarManager: конфигурация панели должна быть словарём, "
                f"получено {type(config).__name__}"
            )
            raise BarConfigurationError(
                bar_id="default",
                parameter="config",
                reason="Конфигурация должна быть словарём",
            )

        if "size" in config:
            size = config["size"]
            if not isinstance(size, int) or size <= 0:
                logger.error(
                    f"BarManager: size должен быть положительным целым числом, "
                    f"получено {size}"
                )
                raise BarConfigurationError(
                    bar_id="default",
                    parameter="size",
                    reason="Ожидалось положительное целое число",
                )

        for color_field in ("background", "border_color"):
            if color_field in config:
                value = config[color_field]
                if not isinstance(value, str) or not value.startswith("#"):
                    logger.error(
                        f"BarManager: {color_field} должен быть hex-цветом, "
                        f"получено {value}"
                    )
                    raise BarConfigurationError(
                        bar_id="default",
                        parameter=color_field,
                        reason=f"Ожидался hex-цвет, получено: {value}",
                    )

        if "opacity" in config:
            opacity = config["opacity"]
            if not isinstance(opacity, (int, float)) or not (0 <= opacity <= 1):
                logger.error(
                    f"BarManager: opacity должен быть числом от 0 до 1, "
                    f"получено {opacity}"
                )
                raise BarConfigurationError(
                    bar_id="default",
                    parameter="opacity",
                    reason="Ожидалось число от 0 до 1",
                )

    def init_bar(self):
        """Создаёт и возвращает объект bar.Bar.

        Returns:
            Объект `libqtile.bar.Bar` или None при отсутствии тем для bar.

        Raises:
            BarInitializationError: При ошибке создания панели.
        """
        themes = self.tc.get_theme_bar()

        if not themes:
            logger.warning("BarManager: темы для bar не найдены, возвращается None")
            return None

        config = self.factory._substitute(themes[0].config)

        self._validate_bar_config(config)

        try:
            result = bar.Bar(widgets=self.widgets, **config)
            logger.info(
                f"BarManager: панель создана, size={config.get('size')}, "
                f"background={config.get('background')}"
            )
            return result
        except Exception as e:
            logger.error(f"BarManager: ошибка создания bar.Bar: {e}")
            raise BarInitializationError(
                bar_id="default",
                reason=str(e),
            ) from e
