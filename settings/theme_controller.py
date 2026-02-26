import json
from pathlib import Path
from config_qtile.theme.theme_model import Theme
from settings.path import QtilePath


class ThemeController:
    def __init__(self, theme_color: str) -> None:
        print(f"🎨 ThemeController инициализируется с темой: {theme_color}")
        self.qp = QtilePath()
        self.theme_path: Path = self.qp.get("config_qtile/theme/presets")

        self.theme_name_layouts = "layouts"
        self.theme_name_widgets = "widgets"
        self.theme_name_bar = "bar"
        self.theme_name_color: str = theme_color

        self.theme_layouts: list[Theme] = self._load_theme_layouts()
        self.theme_widgets: list[Theme] = self._load_theme_widgets()
        self.theme_bar: list[Theme] = self._load_theme_bar()

        # 👇 ВАЖНО: теперь это dict
        self.theme_color: dict = self._load_theme_color()

    # универсальная загрузка для layouts/widgets/bar
    def _load(self, theme_name: str) -> list[Theme]:
        theme_file: Path = self.theme_path / f"{theme_name}.json"
        themes = []

        with open(theme_file) as f:
            data = json.load(f)

            for item in data:
                definition = Theme(
                    name=item.get("name", ""), config=item.get("config", {})
                )
                themes.append(definition)

        return themes

    # 👇 отдельная загрузка цвета (возвращает dict, НЕ list)
    def _load_theme_color(self) -> dict:
        theme_file: Path = self.theme_path / f"{self.theme_name_color}.json"

        with open(theme_file) as f:
            data = json.load(f)

        if not data:
            return {}

        # берём первый пресет
        return data[0].get("config", {})

    def get_theme_color(self) -> dict:
        return self.theme_color

    def _load_theme_layouts(self) -> list[Theme]:
        return self._load(self.theme_name_layouts)

    def get_theme_layouts(self) -> list[Theme]:
        return self.theme_layouts

    def _load_theme_widgets(self) -> list[Theme]:
        return self._load(self.theme_name_widgets)

    def get_theme_widgets(self) -> list[Theme]:
        return self.theme_widgets

    def _load_theme_bar(self) -> list[Theme]:
        return self._load(self.theme_name_bar)

    def get_theme_bar(self) -> list[Theme]:
        return self.theme_bar


# import json
# from pathlib import Path
# from config_qtile.theme.theme_model import Theme
# from settings.path import QtilePath


# class ThemeController:
#     def __init__(self) -> None:
#         self.qp = QtilePath()
#         self.theme_path: Path = self.qp.get("config_qtile/theme/presets")
#         # self.theme_path: Path = (
#         #     Path(__file__).parent.parent / "config_qtile" / "theme" / "presets"
#         # )
#         self.theme_name_layouts = "layouts"
#         self.theme_name_widgets = "widgets"
#         self.theme_name_bar = "bar"
#         self.theme_name_color = "color"
#         self.theme_layouts: list[Theme] = self._load_theme_layouts()
#         self.theme_widgets: list[Theme] = self._load_theme_widgets()
#         self.theme_bar: list[Theme] = self._load_theme_bar()
#         self.theme_color: list[Theme] = self._load_them_color()

#     def _load(self, theme_name: str) -> list:
#         theme_file: Path = self. theme_path / f"{theme_name}.json"
#         themes = []

#         with open(theme_file) as f:
#             data = json.load(f)

#             for item in data:
#                 definition = Theme(
#                     name=item.get("name", ""),
#                     config=item.get("config", {})
#                 )
#                 themes.append(definition)
#         return themes

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

#     def _load_them_color(self) -> list[Theme]:
#         return self._load(self.theme_name_color)

#     def get_theme_color(self) -> list[Theme]:
#         return self.theme_color



