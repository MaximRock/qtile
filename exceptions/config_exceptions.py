"""Исключения, связанные с загрузкой конфигураций."""

from exceptions.base_exceptions import QtileConfigError


class ConfigLoadError(QtileConfigError):
    """Ошибка загрузки конфигурации из JSON файла."""

    def __init__(self, config_name: str, file_path: str, reason: str) -> None:
        self.config_name = config_name
        self.file_path = file_path
        self.reason = reason
        super().__init__(
            f"Не удалось загрузить конфигурацию '{config_name}' из {file_path}: {reason}",
            component="Config"
        )


class ConfigValidationError(QtileConfigError):
    """Ошибка валидации конфигурации."""

    def __init__(self, config_name: str, field: str, reason: str) -> None:
        self.config_name = config_name
        self.field = field
        self.reason = reason
        super().__init__(
            f"Невалидное поле '{field}' в конфигурации '{config_name}': {reason}",
            component="Config"
        )


class ConfigSaveError(QtileConfigError):
    """Ошибка сохранения конфигурации."""

    def __init__(self, config_name: str, file_path: str, reason: str) -> None:
        self.config_name = config_name
        self.file_path = file_path
        self.reason = reason
        super().__init__(
            f"Не удалось сохранить конфигурацию '{config_name}' в {file_path}: {reason}",
            component="Config"
        )
