"""Исключения, связанные с мышью и биндингами."""

from exceptions.base_exceptions import QtileConfigError


class MouseError(QtileConfigError):
    """Базовое исключение для ошибок мыши."""

    def __init__(self, message: str, binding: str | None = None) -> None:
        self.binding = binding
        super().__init__(message, component="Mouse")


class MouseConfigError(MouseError):
    """Ошибка конфигурации мыши."""

    def __init__(self, parameter: str, reason: str) -> None:
        self.parameter = parameter
        self.reason = reason
        super().__init__(
            f"Ошибка конфигурации мыши. Параметр '{parameter}': {reason}"
        )


class MouseBindingError(MouseError):
    """Ошибка биндинга мыши."""

    def __init__(self, binding: str, reason: str) -> None:
        self.binding = binding
        self.reason = reason
        super().__init__(
            f"Невалидный биндинг мыши '{binding}': {reason}",
            binding
        )


class MouseLazyError(MouseError):
    """Ошибка преобразования lazy-команды."""

    def __init__(self, lazy_path: str, reason: str) -> None:
        self.lazy_path = lazy_path
        self.reason = reason
        super().__init__(
            f"Не удалось преобразовать путь lazy-команды '{lazy_path}': {reason}",
            binding=lazy_path
        )
