"""Менеджер виджетов Qtile.

Модуль формирует набор виджетов панели на основе:
- конфигурации темы из `ThemeController`,
- фабричной сборки через `BaseFactory`,
- регистра отображаемых классов виджетов Qtile.
"""

from logging import Logger

from libqtile import widget

from config_qtile.theme.theme_model import Theme
from exceptions.theme_exceptions import ThemeLoadError
from exceptions.widget_exceptions import WidgetConfigurationError, WidgetNotFoundError
from settings.base_factory import BaseFactory
from settings.logger import get_logger
from settings.theme_controller import ThemeController

logger: Logger = get_logger("qtile.default", file="logger")


class WidgetManager:
    """Собирает и возвращает список виджетов для панели Qtile.

    Args:
        theme_controller: Подготовленный экземпляр `ThemeController`.
            Если не передан, будет создан внутри.

    Raises:
        WidgetConfigurationError: При ошибке инициализации темы или фабрики.
    """

    def __init__(self, theme_controller: ThemeController = None) -> None:
        logger.info("Инициализация WidgetManager")
        try:
            self.tc: ThemeController = theme_controller or ThemeController()
            self.colors = self.tc.get_theme_color()
            self.settings = self.tc.get_theme_settings()
            logger.debug(f"Загружены цвета темы: {len(self.colors)} параметров")
            logger.debug(f"Загружены настройки: {len(self.settings)} параметров")
        except ThemeLoadError as e:
            logger.error(f"Ошибка инициализации контроллера темы: {e}")
            raise WidgetConfigurationError(
                widget_name="WidgetManager",
                parameter="theme_controller",
                reason=f"Не удалось инициализировать контроллер темы: {e}"
            ) from e

        themes: list[Theme] = self.tc.get_theme_widgets()
        logger.debug(f"Загружено тем виджетов: {len(themes)}")

        classes: dict[str, object] = {
            "GroupBox": widget.GroupBox,
            "Clock": widget.Clock,
            "WindowName": widget.WindowName,
            "KeyboardLayout": widget.KeyboardLayout,
            "Spacer": widget.Spacer,
            "Systray": widget.Systray,
            "CurrentLayout": widget.CurrentLayout,
            "Prompt": widget.Prompt,
            "CPU": widget.CPU,
            "HDD": widget.HDD,
            "Memory": widget.Memory,
            "Net": widget.Net,
            "Volume": widget.Volume,
            "Battery": widget.Battery,
            "TextBox": widget.TextBox,
            "Sep": widget.Sep,
            "PulseVolume": widget.PulseVolume,
        }

        fallback: list = [widget.GroupBox(), widget.Clock()]
        logger.debug(f"Зарегистрировано виджетов: {len(classes)}")

        try:
            self.factory = BaseFactory(
                themes=themes,
                classes=classes,
                fallback=fallback,
                colors=self.colors,
                settings=self.settings,
            )
            logger.info("Фабрика виджетов успешно создана")
        except Exception as e:
            logger.error(f"Ошибка создания фабрики виджетов: {e}")
            raise WidgetConfigurationError(
                widget_name="WidgetManager",
                parameter="factory",
                reason=f"Не удалось создать фабрику виджетов: {e}"
            ) from e

    def get_widget(self):
        """Собирает и возвращает итоговый список виджетов.

        Returns:
            Список сконфигурированных объектов виджетов Qtile.

        Raises:
            WidgetNotFoundError: Если сборка виджетов завершилась ошибкой.
        """
        logger.debug("Сборка виджетов")
        try:
            widgets = self.factory.build()
            logger.info(f"Виджеты успешно собраны: {len(widgets)} шт.")
            return widgets
        except Exception as e:
            logger.error(f"Ошибка сборки виджетов: {e}")
            raise WidgetNotFoundError(
                widget_name="unknown",
                available_widgets=list(self.factory.classes.keys())
            ) from e
