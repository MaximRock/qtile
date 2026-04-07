"""Исключения, связанные с привязками клавиш."""

from exceptions.base_exceptions import QtileConfigError


class KeyBindingError(QtileConfigError):
    """Базовое исключение для ошибок привязок клавиш."""

    def __init__(self, message: str, key_combination: str | None = None) -> None:
        self.key_combination = key_combination
        super().__init__(message, component="KeyBinding")


class KeyBindingConflictError(KeyBindingError):
    """Конфликт привязок клавиш."""

    def __init__(self, key_combination: str, existing_action: str, new_action: str) -> None:
        self.key_combination = key_combination
        self.existing_action = existing_action
        self.new_action = new_action
        super().__init__(
            f"Конфликт привязки '{key_combination}': уже назначено на '{existing_action}', "
            f"попытка переназначить на '{new_action}'",
            key_combination
        )


class KeyBindingFormatError(KeyBindingError):
    """Ошибка формата комбинации клавиш."""

    def __init__(self, key_combination: str, reason: str) -> None:
        self.key_combination = key_combination
        self.reason = reason
        super().__init__(
            f"Невалидный формат комбинации '{key_combination}': {reason}",
            key_combination
        )


class KeyBindingExecutionError(KeyBindingError):
    """Ошибка выполнения действия привязки."""

    def __init__(self, key_combination: str, action: str, reason: str) -> None:
        self.key_combination = key_combination
        self.action = action
        self.reason = reason
        super().__init__(
            f"Не удалось выполнить действие '{action}' для привязки '{key_combination}': {reason}",
            key_combination
        )
