"""Исключения, связанные с виджетами."""

from exceptions.base_exceptions import QtileConfigError


class WidgetError(QtileConfigError):
    """Базовое исключение для ошибок виджетов."""

    def __init__(self, message: str, widget_name: str | None = None) -> None:
        self.widget_name = widget_name
        super().__init__(message, component="Widget")


class WidgetNotFoundError(WidgetError):
    """Виджет не найден."""

    def __init__(self, widget_name: str, available_widgets: list[str] | None = None) -> None:
        self.widget_name = widget_name
        self.available_widgets = available_widgets or []
        message = f"Виджет '{widget_name}' не найден"
        if self.available_widgets:
            message += f". Доступные виджеты: {', '.join(self.available_widgets)}"
        super().__init__(message, widget_name)


class WidgetConfigurationError(WidgetError):
    """Ошибка конфигурации виджета."""

    def __init__(self, widget_name: str, parameter: str, reason: str) -> None:
        self.widget_name = widget_name
        self.parameter = parameter
        self.reason = reason
        super().__init__(
            f"Невалидный параметр '{parameter}' для виджета '{widget_name}': {reason}",
            widget_name
        )


class WidgetPlacementError(WidgetError):
    """Ошибка размещения виджета на панели."""

    def __init__(self, widget_name: str, bar_position: str, reason: str) -> None:
        self.widget_name = widget_name
        self.bar_position = bar_position
        self.reason = reason
        super().__init__(
            f"Не удалось разместить виджет '{widget_name}' на панели ({bar_position}): {reason}",
            widget_name
        )
