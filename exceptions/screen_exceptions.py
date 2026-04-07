"""Исключения, связанные с экранами и мониторами."""

from exceptions.base_exceptions import QtileConfigError


class ScreenError(QtileConfigError):
    """Базовое исключение для ошибок экранов."""

    def __init__(self, message: str, screen_id: int | None = None) -> None:
        self.screen_id = screen_id
        super().__init__(message, component="Screen")


class ScreenNotFoundError(ScreenError):
    """Экран не найден."""

    def __init__(self, screen_id: int | str, available_screens: list[int] | None = None) -> None:
        self.screen_id = screen_id
        self.available_screens = available_screens or []
        message = f"Экран '{screen_id}' не найден"
        if self.available_screens:
            message += f". Доступные экраны: {self.available_screens}"
        super().__init__(message, screen_id)


class ScreenConfigurationError(ScreenError):
    """Ошибка конфигурации экрана."""

    def __init__(self, screen_id: int | str, parameter: str, reason: str) -> None:
        self.screen_id = screen_id
        self.parameter = parameter
        self.reason = reason
        super().__init__(
            f"Невалидный параметр '{parameter}' для экрана '{screen_id}': {reason}",
            screen_id
        )


class BarConfigurationError(ScreenError):
    """Ошибка конфигурации панели."""

    def __init__(self, screen_id: int | str, position: str, reason: str) -> None:
        self.screen_id = screen_id
        self.position = position
        self.reason = reason
        super().__init__(
            f"Не удалось настроить панель на экране '{screen_id}' (позиция: {position}): {reason}",
            screen_id
        )
