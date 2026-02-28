# settings/base_factory.py

import json
import re
from typing import Any

HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


class BaseFactory:
    def __init__(
        self,
        themes: list,
        classes: dict[str, type],
        fallback: list | None = None,
        colors: dict | None = None,
        settings: dict | None = None,
    ):
        self.themes = themes
        self.classes = classes
        self.fallback = fallback or []
        self.colors = colors or {}
        self.settings = settings or {}

    def _validate_color(self, value: str, key: str = "") -> str:
        """Проверка, что строка — корректный hex-цвет."""
        if not HEX_COLOR_RE.match(value):
            raise ValueError(f"Invalid color value for '{key}': {value}")
        return value

    def _convert_type(self, value: str, original_value: Any) -> Any:
        """
        Преобразует строку обратно в исходный тип.
        """
        # Если оригинал был числом
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
        """Рекурсивная замена значений с преобразованием типов."""
        if variables is None:
            variables = {**self.colors, **self.settings}

        if isinstance(value, str):
            value = value.strip().strip("'").strip('"')

            # {placeholder}
            if value.startswith("{") and value.endswith("}"):
                var_key = value[1:-1]
                resolved = variables.get(var_key, value)

                # ✅ Преобразуем тип если нужно
                if isinstance(resolved, (int, float, bool)):
                    return resolved

                if isinstance(resolved, str) and resolved.startswith("#"):
                    self._validate_color(resolved, config_key)
                return resolved

            # Прямая ссылка на переменную
            if value in variables:
                resolved = variables[value]

                # ✅ Преобразуем тип если нужно
                if isinstance(resolved, (int, float, bool)):
                    return resolved

                if isinstance(resolved, str) and resolved.startswith("#"):
                    self._validate_color(resolved, config_key)
                return resolved

            # Hex-цвет
            if value.startswith("#"):
                self._validate_color(value, config_key)

            return value

        elif isinstance(value, list):
            return [self._substitute_value(v, config_key, variables) for v in value]

        elif isinstance(value, dict):
            return {
                k: self._substitute_value(v, k, variables) for k, v in value.items()
            }

        return value

    def _substitute(self, config: dict) -> dict:
        """Подставляет переменные во все значения конфига."""
        return {
            key: self._substitute_value(value, key) for key, value in config.items()
        }

    def build(self) -> list:
        """Создаёт объекты с подставленными значениями."""
        items = []

        for theme in self.themes:
            cls = self.classes.get(theme.name)
            if not cls:
                print(f"⚠️ Класс '{theme.name}' не найден")
                continue

            final_config = self._substitute(theme.config)

            try:
                items.append(cls(**final_config))
                print(f"✅ Создан: {theme.name}")
            except Exception as e:
                print(f"❌ Ошибка создания {theme.name}: {e}")

        if not items and self.fallback:
            print(f"⚠️ Используется fallback ({len(self.fallback)} элементов)")
            return self.fallback

        return items




# import json
# import re

# HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


# class BaseFactory:
#     def __init__(
#         self,
#         themes: list,
#         classes: dict,
#         fallback: list | None = None,
#         colors: dict | None = None,
#     ):
#         self.themes = themes
#         self.classes = classes
#         self.fallback = fallback or []
#         self.colors = colors or {}

#     def _validate_color(self, value: str) -> str:
#         """Проверка, что строка — корректный hex-цвет."""
#         if not HEX_COLOR_RE.match(value):
#             raise ValueError(f"Invalid color value: {value}")
#         return value

#     def _substitute(self, config: dict) -> dict:
#         """
#         Подставляет {variables} из colors в config
#         и проверяет правильность hex-цветов.
#         """
#         if not self.colors:
#             return config

#         config_str = json.dumps(config)

#         for key, value in self.colors.items():
#             placeholder = f"{{{key}}}"
#             # Проверка цвета только если это строка с #
#             if isinstance(value, str) and value.startswith("#"):
#                 self._validate_color(value)
#             config_str = config_str.replace(placeholder, str(value))

#         return json.loads(config_str)

#     def build(self) -> list:
#         """
#         Создаёт виджеты/классы с подставленными цветами.
#         """
#         items = []

#         for theme in self.themes:
#             cls = self.classes.get(theme.name)
#             if not cls:
#                 continue

#             # Подставляем переменные
#             final_config = self._substitute(theme.config)

#             try:
#                 items.append(cls(**final_config))
#             except Exception as e:
#                 print(f"Error creating widget {theme.name}: {e}")

#         if not items and self.fallback:
#             return self.fallback
#         return items


# import json


# class BaseFactory:
#     def __init__(
#         self,
#         themes,
#         classes: dict,
#         fallback: list | None,
#         colors: dict | None = None,
#     ):
#         self.themes = themes
#         self.classes = classes
#         self.fallback = fallback
#         self.colors = colors or {}

#     def _substitute(self, config: dict) -> dict:
#         """
#         Подставляет {variables} из colors в config
#         """
#         if not self.colors:
#             return config

#         config_str = json.dumps(config)

#         for key, value in self.colors.items():
#             placeholder = f"{{{key}}}"
#             config_str = config_str.replace(placeholder, str(value))

#         return json.loads(config_str)

#     def build(self):
#         items = []

#         for theme in self.themes:
#             cls = self.classes.get(theme.name)
#             if not cls:
#                 continue

#             # 👇 вот здесь происходит магия
#             final_config = self._substitute(theme.config)

#             items.append(cls(**final_config))

#         return items if items else self.fallback


# class BaseFactory:
#     def __init__(self, themes, classes: dict, fallback: list | None):
#         self.themes = themes
#         self.classes = classes
#         self.fallback = fallback

#     def build(self):
#         items = []

#         for theme in self.themes:
#             cls = self.classes.get(theme.name)
#             if cls:
#                 items.append(cls(**theme.config))

#         return items if items else self.fallback
