"""Фабрика для создания объектов конфигурации Qtile с подстановкой переменных.

Модуль предоставляет класс `BaseFactory`, который:
- принимает список тем (themes), словарь классов (classes), fallback-объекты;
- подставляет переменные вида `{key}` или `key` из словарей colors/settings;
- валидирует hex-цвета;
- создаёт объекты указанных классов с подставленными конфигами.

При ошибках используются исключения из `exceptions/factory_exceptions.py`.
"""

import re
from logging import Logger
from typing import Any

from exceptions.factory_exceptions import (
    FactoryInstantiationError,
    FactoryValidationError,
)
from settings.logger import get_logger

logger: Logger = get_logger("qtile.basefactory", file="basefactory")

HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


class BaseFactory:
    """Фабрика для создания объектов с подстановкой переменных.

    Args:
        themes: Список объектов Theme с конфигурацией.
        classes: Словарь имя_класса -> класс для создания объектов.
        fallback: Список объектов, используемых при отсутствии результата.
        colors: Словарь цветовых переменных для подстановки.
        settings: Словарь настроек для подстановки.
    """

    def __init__(
        self,
        themes: list,
        classes: dict[str, type],
        fallback: list | None = None,
        colors: dict | None = None,
        settings: dict | None = None,
    ) -> None:
        self.themes = themes
        self.classes = classes
        self.fallback = fallback or []
        self.colors = colors or {}
        self.settings = settings or {}

        logger.debug(
            f"BaseFactory инициализирована: {len(themes)} тем, "
            f"{len(classes)} классов, {len(self.fallback)} fallback"
        )

    def _validate_color(self, value: str, key: str = "") -> str:
        """Валидирует, что значение является корректным hex-цветом."""
        if not HEX_COLOR_RE.match(value):
            logger.error(f"BaseFactory: невалидный hex-цвет для '{key}': {value}")
            raise FactoryValidationError(
                factory_name="BaseFactory",
                field=key,
                reason=f"Невалидный hex-цвет: {value}",
            )
        return value

    def _convert_type(self, value: str, original_value: Any) -> Any:
        """Преобразует строковое значение к типу оригинального значения."""
        if isinstance(original_value, int):
            try:
                return int(value)
            except (ValueError, TypeError):
                return value
        elif isinstance(original_value, float):
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        elif isinstance(original_value, bool):
            return value.lower() in ("true", "1", "yes")
        return value

    def _substitute_value(
        self, value: Any, config_key: str = "", variables: dict = None
    ) -> Any:
        """Рекурсивно подставляет переменные в значение."""
        if variables is None:
            variables = {**self.colors, **self.settings}

        if isinstance(value, str):
            value = value.strip().strip("'").strip('"')

            # {placeholder}
            if value.startswith("{") and value.endswith("}"):
                var_key = value[1:-1]
                resolved = variables.get(var_key, value)
                logger.debug(f"BaseFactory подстановка {config_key}: {value} -> {resolved}")
                if isinstance(resolved, str) and resolved.startswith("#"):
                    self._validate_color(resolved, config_key)
                if resolved == value:
                    logger.warning(
                        f"BaseFactory: плейсхолдер '{value}' не найден в переменных"
                    )
                return resolved

            # прямая переменная
            if value in variables:
                resolved = variables[value]
                logger.debug(f"BaseFactory подстановка {config_key}: {value} -> {resolved}")
                if isinstance(resolved, str) and resolved.startswith("#"):
                    self._validate_color(resolved, config_key)
                return resolved

            # hex-цвет
            if value.startswith("#"):
                self._validate_color(value, config_key)

            return value

        elif isinstance(value, list):
            return [self._substitute_value(v, config_key, variables) for v in value]
        elif isinstance(value, dict):
            return {k: self._substitute_value(v, k, variables) for k, v in value.items()}

        return value

    def _substitute(self, config: dict) -> dict:
        """Подставляет переменные во все значения конфига."""
        return {key: self._substitute_value(value, key) for key, value in config.items()}

    def build(self) -> list:
        """Создаёт объекты с подставленными значениями.

        Returns:
            Список созданных объектов или fallback-объекты при отсутствии результата.
        """
        items = []

        for theme in self.themes:
            cls = self.classes.get(theme.name)
            if not cls:
                logger.error(f"BaseFactory: класс для темы '{theme.name}' не найден")
                continue

            final_config = self._substitute(theme.config)

            try:
                items.append(cls(**final_config))
                logger.info(f"BaseFactory: создан объект '{theme.name}'")
            except Exception as e:
                logger.error(f"BaseFactory: ошибка создания объекта '{theme.name}': {e}")
                raise FactoryInstantiationError(
                    factory_name="BaseFactory",
                    class_name=theme.name,
                    reason=str(e),
                ) from e

        if not items and self.fallback:
            logger.warning(
                f"BaseFactory: используется fallback ({len(self.fallback)} элементов)"
            )
            return self.fallback

        if not items:
            logger.error(
                "BaseFactory: не создано ни одного объекта и fallback недоступен"
            )

        return items
