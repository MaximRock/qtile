import re
from typing import Any

from settings.loger import get_logger

HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

logger = get_logger("qtile.basefactory", file="basefactory")


class BaseFactory:
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

    def _validate_color(self, value: str, key: str = "") -> str:
        if not HEX_COLOR_RE.match(value):
            logger.error(f"Invalid color value for '{key}': {value}")
            raise ValueError(f"Invalid color value for '{key}': {value}")
        return value

    def _convert_type(self, value: str, original_value: Any) -> Any:
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
        if variables is None:
            variables = {**self.colors, **self.settings}

        if isinstance(value, str):
            value = value.strip().strip("'").strip('"')

            # {placeholder}
            if value.startswith("{") and value.endswith("}"):
                var_key = value[1:-1]
                resolved = variables.get(var_key, value)
                logger.debug(f"Substitute {config_key}: {value} -> {resolved}")
                if isinstance(resolved, str) and resolved.startswith("#"):
                    self._validate_color(resolved, config_key)
                return resolved

            # прямая переменная
            if value in variables:
                resolved = variables[value]
                logger.debug(f"Substitute {config_key}: {value} -> {resolved}")
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
        return {key: self._substitute_value(value, key) for key, value in config.items()}

    def build(self) -> list:
        items = []

        for theme in self.themes:
            cls = self.classes.get(theme.name)
            if not cls:
                logger.error(f"Class '{theme.name}' not found")
                continue

            final_config = self._substitute(theme.config)

            try:
                items.append(cls(**final_config))
                logger.info(f"✅ Created object: {theme.name}")
            except Exception as e:
                logger.exception(f"Error creating object {theme.name}: {e}")

        if not items and self.fallback:
            logger.warning(f"Using fallback ({len(self.fallback)} items)")
            return self.fallback

        return items





# import re
# from typing import Any

# HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


# class BaseFactory:
#     def __init__(
#         self,
#         themes: list,
#         classes: dict[str, type],
#         fallback: list | None = None,
#         colors: dict | None = None,
#         settings: dict | None = None,
#     ):
#         self.themes = themes
#         self.classes = classes
#         self.fallback = fallback or []
#         self.colors = colors or {}
#         self.settings = settings or {}

#     def _validate_color(self, value: str, key: str = "") -> str:
#         """Проверка, что строка — корректный hex-цвет."""
#         if not HEX_COLOR_RE.match(value):
#             raise ValueError(f"Invalid color value for '{key}': {value}")
#         return value

#     def _convert_type(self, value: str, original_value: Any) -> Any:
#         """
#         Преобразует строку обратно в исходный тип.
#         """
#         # Если оригинал был числом
#         if isinstance(original_value, int):
#             try:
#                 return int(value)
#             except (ValueError, TypeError):
#                 return value
#         elif isinstance(original_value, float):
#             try:
#                 return float(value)
#             except (ValueError, TypeError):
#                 return value
#         elif isinstance(original_value, bool):
#             return value.lower() in ("true", "1", "yes")
#         return value

#     def _substitute_value(
#         self, value: Any, config_key: str = "", variables: dict = None
#     ) -> Any:
#         """Рекурсивная замена значений с преобразованием типов."""
#         if variables is None:
#             variables = {**self.colors, **self.settings}

#         if isinstance(value, str):
#             value = value.strip().strip("'").strip('"')

#             # {placeholder}
#             if value.startswith("{") and value.endswith("}"):
#                 var_key = value[1:-1]
#                 resolved = variables.get(var_key, value)

#                 # Преобразуем тип если нужно
#                 if isinstance(resolved, (int, float, bool)):
#                     return resolved

#                 if isinstance(resolved, str) and resolved.startswith("#"):
#                     self._validate_color(resolved, config_key)
#                 return resolved

#             # Прямая ссылка на переменную
#             if value in variables:
#                 resolved = variables[value]

#                 # Преобразуем тип если нужно
#                 if isinstance(resolved, (int, float, bool)):
#                     return resolved

#                 if isinstance(resolved, str) and resolved.startswith("#"):
#                     self._validate_color(resolved, config_key)
#                 return resolved

#             # Hex-цвет
#             if value.startswith("#"):
#                 self._validate_color(value, config_key)

#             return value

#         elif isinstance(value, list):
#             return [self._substitute_value(v, config_key, variables) for v in value]

#         elif isinstance(value, dict):
#             return {
#                 k: self._substitute_value(v, k, variables) for k, v in value.items()
#             }

#         return value

#     def _substitute(self, config: dict) -> dict:
#         """Подставляет переменные во все значения конфига."""
#         return {
#             key: self._substitute_value(value, key) for key, value in config.items()
#         }

#     def build(self) -> list:
#         """Создаёт объекты с подставленными значениями."""
#         items = []

#         for theme in self.themes:
#             cls = self.classes.get(theme.name)
#             if not cls:
#                 print(f"Класс '{theme.name}' не найден")
#                 continue

#             final_config = self._substitute(theme.config)

#             try:
#                 items.append(cls(**final_config))
#                 print(f"✅ Создан: {theme.name}")
#             except Exception as e:
#                 print(f"Ошибка создания {theme.name}: {e}")

#         if not items and self.fallback:
#             print(f"Используется fallback ({len(self.fallback)} элементов)")
#             return self.fallback

#         return items
