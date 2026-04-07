"""Исключения, связанные с раскладками."""

from exceptions.base_exceptions import QtileConfigError


class LayoutError(QtileConfigError):
    """Базовое исключение для ошибок раскладок."""

    def __init__(self, message: str, layout_name: str | None = None) -> None:
        self.layout_name = layout_name
        super().__init__(message, component="Layout")


class LayoutNotFoundError(LayoutError):
    """Раскладка не найдена."""

    def __init__(self, layout_name: str, available_layouts: list[str] | None = None) -> None:
        self.layout_name = layout_name
        self.available_layouts = available_layouts or []
        message = f"Раскладка '{layout_name}' не найдена"
        if self.available_layouts:
            message += f". Доступные раскладки: {', '.join(self.available_layouts)}"
        super().__init__(message, layout_name)


class LayoutConfigurationError(LayoutError):
    """Ошибка конфигурации раскладки."""

    def __init__(self, layout_name: str, parameter: str, reason: str) -> None:
        self.layout_name = layout_name
        self.parameter = parameter
        self.reason = reason
        super().__init__(
            f"Невалидный параметр '{parameter}' для раскладки '{layout_name}': {reason}",
            layout_name
        )


class LayoutSwitchError(LayoutError):
    """Ошибка переключения раскладки."""

    def __init__(self, from_layout: str, to_layout: str, reason: str) -> None:
        self.from_layout = from_layout
        self.to_layout = to_layout
        self.reason = reason
        super().__init__(
            f"Не удалось переключить раскладку с '{from_layout}' на '{to_layout}': {reason}",
            layout_name=to_layout
        )
