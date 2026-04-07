"""Исключения, связанные с путями к файлам."""

from exceptions.base_exceptions import QtileConfigError


class PathError(QtileConfigError):
    """Базовое исключение для ошибок путей."""

    def __init__(self, message: str, path: str | None = None) -> None:
        self.path = path
        super().__init__(message, component="Path")


class PathNotFoundError(PathError):
    """Путь не найден."""

    def __init__(self, path: str, expected_type: str = "file") -> None:
        self.path = path
        self.expected_type = expected_type
        super().__init__(f"{expected_type.capitalize()} не найден: {path}", path)


class PathPermissionError(PathError):
    """Ошибка доступа к пути."""

    def __init__(self, path: str, operation: str) -> None:
        self.path = path
        self.operation = operation
        super().__init__(
            f"Нет прав на {operation} пути '{path}'",
            path
        )


class PathResolutionError(PathError):
    """Ошибка разрешения пути."""

    def __init__(self, base_path: str, relative_path: str, reason: str) -> None:
        self.base_path = base_path
        self.relative_path = relative_path
        self.reason = reason
        super().__init__(
            f"Не удалось разрешить путь '{relative_path}' относительно '{base_path}': {reason}",
            base_path
        )
