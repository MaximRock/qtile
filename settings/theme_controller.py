# settings/theme_controller.py

import json
from pathlib import Path

from config_qtile.theme.theme_model import Theme
from settings.path import QtilePath


# settings/theme_controller.py


class ThemeController:
    def __init__(self, theme_color: str) -> None:
        print(f"🎨 ThemeController инициализируется с темой: {theme_color}")
        self.qp = QtilePath()
        self.theme_path: Path = self.qp.get("config_qtile/theme/settings_json")
        self.theme_color_path: Path = self.qp.get("config_qtile/theme/presets")

        self.theme_name_layouts = "layouts"
        self.theme_name_widgets = "widgets"
        self.theme_name_bar = "bar"
        self.theme_name_color: str = theme_color

        # ✅ Загружаем общие настройки
        self.theme_settings: dict = self._load_theme_settings()

        # ✅ Загружаем конфигурации (методы должны существовать!)
        self.theme_layouts: list[Theme] = self._load_theme_layouts()
        self.theme_widgets: list[Theme] = self._load_theme_widgets()
        self.theme_bar: list[Theme] = self._load_theme_bar()

        # ✅ Загружаем цвета
        self.theme_color: dict = self._load_theme_color()

    def _load_theme_settings(self) -> dict:
        """Загружает общие настройки из base.json"""
        theme_file: Path = self.theme_path / "base.json"
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ Загружены настройки: {theme_file}")
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Ошибка загрузки settings.json: {e}")
            return {}

    def _load(self, theme_name: str) -> list[Theme]:
        """Загружает конфигурацию виджетов/layouts/bar"""
        theme_file: Path = self.theme_path / f"{theme_name}.json"
        themes = []

        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    definition = Theme(
                        name=item.get("name", ""), config=item.get("config", {})
                    )
                    themes.append(definition)
            print(f"✅ Загружено: {theme_name}.json ({len(themes)} элементов)")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Ошибка загрузки {theme_name}.json: {e}")

        return themes

    def _load_theme_layouts(self) -> list[Theme]:
        """✅ Метод должен существовать!"""
        return self._load(self.theme_name_layouts)

    def _load_theme_widgets(self) -> list[Theme]:
        """✅ Метод должен существовать!"""
        return self._load(self.theme_name_widgets)

    def _load_theme_bar(self) -> list[Theme]:
        """✅ Метод должен существовать!"""
        return self._load(self.theme_name_bar)

    def _load_theme_color(self) -> dict:
        """Загружает цветовую схему"""
        theme_file: Path = self.theme_color_path / f"{self.theme_name_color}.json"
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ Загружена тема: {theme_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Ошибка загрузки темы: {e}")
            return {}

        if not data:
            return {}

        return data[0].get("config", {})

    def get_theme_settings(self) -> dict:
        return self.theme_settings

    def get_theme_layouts(self) -> list[Theme]:
        return self.theme_layouts

    def get_theme_widgets(self) -> list[Theme]:
        return self.theme_widgets

    def get_theme_bar(self) -> list[Theme]:
        return self.theme_bar

    def get_theme_color(self) -> dict:
        return self.theme_color




# import json
# from pathlib import Path

# from config_qtile.theme.theme_model import Theme
# from settings.path import QtilePath


# class ThemeController:
#     def __init__(self, theme_color: str) -> None:
#         print(f"🎨 ThemeController инициализируется с темой: {theme_color}")
#         self.qp = QtilePath()
#         self.theme_path: Path = self.qp.get("config_qtile/theme/settings_json")
#         self.theme_color_path: Path = self.qp.get("config_qtile/theme/presets")

#         self.theme_name_layouts = "layouts"
#         self.theme_name_widgets = "widgets"
#         self.theme_name_bar = "bar"
#         self.theme_name_color: str = theme_color

#         self.theme_layouts: list[Theme] = self._load_theme_layouts()
#         self.theme_widgets: list[Theme] = self._load_theme_widgets()
#         self.theme_bar: list[Theme] = self._load_theme_bar()

#         self.theme_color: dict = self._load_theme_color()

#     def _load(self, theme_name: str) -> list[Theme]:
#         theme_file: Path = self.theme_path / f"{theme_name}.json"
#         themes = []

#         with open(theme_file) as f:
#             data = json.load(f)

#             for item in data:
#                 definition = Theme(
#                     name=item.get("name", ""), config=item.get("config", {})
#                 )
#                 themes.append(definition)

#         return themes

#     def _load_theme_color(self) -> dict:
#         theme_file: Path = self.theme_color_path / f"{self.theme_name_color}.json"

#         with open(theme_file) as f:
#             data = json.load(f)

#         if not data:
#             return {}

#         return data[0].get("config", {})

#     def get_theme_color(self) -> dict:
#         return self.theme_color

#     def _load_theme_layouts(self) -> list[Theme]:
#         return self._load(self.theme_name_layouts)

#     def get_theme_layouts(self) -> list[Theme]:
#         return self.theme_layouts

#     def _load_theme_widgets(self) -> list[Theme]:
#         return self._load(self.theme_name_widgets)

#     def get_theme_widgets(self) -> list[Theme]:
#         return self.theme_widgets

#     def _load_theme_bar(self) -> list[Theme]:
#         return self._load(self.theme_name_bar)

#     def get_theme_bar(self) -> list[Theme]:
#         return self.theme_bar
