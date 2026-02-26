import json
import re

HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


class BaseFactory:
    def __init__(
        self,
        themes: list,
        classes: dict,
        fallback: list | None = None,
        colors: dict | None = None,
    ):
        self.themes = themes
        self.classes = classes
        self.fallback = fallback or []
        self.colors = colors or {}

    def _validate_color(self, value: str) -> str:
        """Проверка, что строка — корректный hex-цвет."""
        if not HEX_COLOR_RE.match(value):
            raise ValueError(f"Invalid color value: {value}")
        return value

    def _substitute(self, config: dict) -> dict:
        """
        Подставляет {variables} из colors в config
        и проверяет правильность hex-цветов.
        """
        if not self.colors:
            return config

        config_str = json.dumps(config)

        for key, value in self.colors.items():
            placeholder = f"{{{key}}}"
            # Проверка цвета только если это строка с #
            if isinstance(value, str) and value.startswith("#"):
                self._validate_color(value)
            config_str = config_str.replace(placeholder, str(value))

        return json.loads(config_str)

    def build(self) -> list:
        """
        Создаёт виджеты/классы с подставленными цветами.
        """
        items = []

        for theme in self.themes:
            cls = self.classes.get(theme.name)
            if not cls:
                continue

            # Подставляем переменные
            final_config = self._substitute(theme.config)

            try:
                items.append(cls(**final_config))
            except Exception as e:
                print(f"Error creating widget {theme.name}: {e}")

        if not items and self.fallback:
            return self.fallback
        return items


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
