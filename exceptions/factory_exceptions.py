"""Исключения, связанные с фабриками и созданием объектов конфигурации."""

from exceptions.base_exceptions import QtileConfigError


class FactoryError(QtileConfigError):
    """Базовое исключение для ошибок фабрики."""

    def __init__(self, message: str, factory_name: str | None = None) -> None:
        self.factory_name = factory_name
        super().__init__(message, component="Factory")


class FactoryInstantiationError(FactoryError):
    """Ошибка создания объекта через фабрику."""

    def __init__(self, factory_name: str, class_name: str, reason: str) -> None:
        self.class_name = class_name
        self.reason = reason
        super().__init__(
            f"Не удалось создать экземпляр класса '{class_name}' в фабрике '{factory_name}': {reason}",
            factory_name
        )


class FactoryRegistrationError(FactoryError):
    """Ошибка регистрации класса в фабрике."""

    def __init__(self, factory_name: str, class_name: str, reason: str) -> None:
        self.class_name = class_name
        self.reason = reason
        super().__init__(
            f"Не удалось зарегистрировать класс '{class_name}' в фабрике '{factory_name}': {reason}",
            factory_name
        )


class FactorySubstitutionError(FactoryError):
    """Ошибка подстановки переменных в конфигурацию."""

    def __init__(self, factory_name: str, key: str, value: str, reason: str) -> None:
        self.key = key
        self.value = value
        self.reason = reason
        super().__init__(
            f"Не удалось подставить значение для ключа '{key}' в фабрике '{factory_name}': {reason}",
            factory_name
        )


class FactoryValidationError(FactoryError):
    """Ошибка валидации данных в фабрике."""

    def __init__(self, factory_name: str, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(
            f"Ошибка валидации поля '{field}' в фабрике '{factory_name}': {reason}",
            factory_name
        )
