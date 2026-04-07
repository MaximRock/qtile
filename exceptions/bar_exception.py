"""Исключения, связанные с панелями (bar) и их конфигурацией."""

from exceptions.base_exceptions import QtileConfigError


class BarError(QtileConfigError):
    """Базовое исключение для ошибок панелей."""

    def __init__(self, message: str, bar_id: str | None = None) -> None:
        self.bar_id = bar_id
        super().__init__(message, component="Bar")


class BarConfigurationError(BarError):
    """Ошибка конфигурации панели."""

    def __init__(self, bar_id: str, parameter: str, reason: str) -> None:
        self.bar_id = bar_id
        self.parameter = parameter
        self.reason = reason
        super().__init__(
            f"Невалидный параметр '{parameter}' для панели '{bar_id}': {reason}",
            bar_id
        )


class BarWidgetError(BarError):
    """Ошибка виджета внутри панели."""

    def __init__(self, bar_id: str, widget_name: str, reason: str) -> None:
        self.widget_name = widget_name
        self.reason = reason
        super().__init__(
            f"Ошибка виджета '{widget_name}' в панели '{bar_id}': {reason}",
            bar_id
        )


class BarInitializationError(BarError):
    """Ошибка инициализации панели."""

    def __init__(self, bar_id: str, reason: str) -> None:
        self.bar_id = bar_id
        self.reason = reason
        super().__init__(
            f"Не удалось инициализировать панель '{bar_id}': {reason}",
            bar_id
        )
