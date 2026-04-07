"""Исключения, связанные с темой и цветовыми схемами."""

from exceptions.base_exceptions import QtileConfigError


class ThemeError(QtileConfigError):
    """Базовое исключение для ошибок темы."""

    def __init__(self, message: str, theme_name: str | None = None) -> None:
        self.theme_name: str | None = theme_name
        super().__init__(message, component="Theme")


class ThemeNotFoundError(ThemeError):
    """Тема не найдена в доступных пресетах."""

    def __init__(self, theme_name: str, available_themes: list[str] | None = None) -> None:
        self.theme_name: str = theme_name
        self.available_themes = available_themes or []
        message: str = f"Тема '{theme_name}' не найдена"
        if self.available_themes:
            message += f". Доступные темы: {', '.join(self.available_themes)}"
        super().__init__(message, theme_name)


class ThemeLoadError(ThemeError):
    """Ошибка загрузки файла темы."""

    def __init__(self, theme_name: str, file_path: str, reason: str) -> None:
        self.file_path: str = file_path
        self.reason: str = reason
        super().__init__(f"Не удалось загрузить тему '{theme_name}': {reason}", theme_name)


class ThemeValidationError(ThemeError):
    """Ошибка валидации данных темы."""

    def __init__(self, theme_name: str, field: str, reason: str) -> None:
        self.field: str = field
        self.reason: str = reason
        super().__init__(
            f"Невалидное поле '{field}' в теме '{theme_name}': {reason}",
            theme_name
        )
