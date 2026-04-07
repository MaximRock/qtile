"""Базовые исключения для конфигурации Qtile.

Централизованная система исключений для обработки ошибок
в модульной архитектуре конфигурации Qtile.

Пример использования:
    from exeptions.theme_exceptions import ThemeNotFoundError, ThemeLoadError
    from exeptions.config_exceptions import ConfigLoadError
    from exeptions.factory_exceptions import FactorySubstitutionError
"""


class QtileConfigError(Exception):
    """Базовое исключение для всех ошибок конфигурации Qtile.

    Все специализированные исключения наследуются от этого класса.
    """

    def __init__(self, message: str, component: str | None = None) -> None:
        self.component = component
        self.message = f"[{component}] {message}" if component else message
        super().__init__(self.message)
