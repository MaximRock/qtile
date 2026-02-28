# settings/bar.py

from libqtile import bar
from settings.theme_controller import ThemeController
from settings.widgets import WidgetManager
from settings.base_factory import BaseFactory


class BarManager:
    def __init__(self, theme_controller: ThemeController = None) -> None:
        self.tc = theme_controller or ThemeController()
        self.colors = self.tc.get_theme_color()
        self.settings = self.tc.get_theme_settings()  # ✅ Получаем настройки

        self.widgets = WidgetManager(theme_controller=self.tc).get_widget()

        self.factory = BaseFactory(
            themes=self.tc.get_theme_bar(),
            classes={},
            fallback=[],
            colors=self.colors,
            settings=self.settings,  # ✅ Передаём настройки
        )

    def init_bar(self):
        themes = self.tc.get_theme_bar()
        if not themes:
            return None

        config = self.factory._substitute(themes[0].config)
        return bar.Bar(widgets=self.widgets, **config)




# from libqtile import bar

# from config_qtile.theme.theme_model import Theme
# from settings.base_factory import BaseFactory
# from settings.theme_controller import ThemeController
# from settings.widgets import WidgetManager


# class BarManager:
#     def __init__(self, theme_controller: ThemeController = None) -> None:
#         self.tc = theme_controller

#         self.widgets = WidgetManager(theme_controller=self.tc).get_widget()

#         self.factory = BaseFactory(
#             themes=self.tc.get_theme_bar(),
#             classes={},
#             fallback=[],
#             colors=self.tc.get_theme_color(),
#         )

#     def init_bar(self):
#         themes = self.tc.get_theme_bar()

#         if not themes:
#             return None

#         config = self.factory._substitute(themes[0].config)

#         return bar.Bar(widgets=self.widgets, **config)


# class BarManager:
#     def __init__(self) -> None:
#         self.bar_theme = ThemeController().get_theme_bar()
#         self.widget = WidgetManager().get_widget()
#         self.factory = BaseFactory(
#             themes=self.bar_theme,
#             classes={"Bar": bar.Bar},
#             fallback=[]
#         )

#     def init_bar(self):

#         if self.bar_theme:
#             bar_config = self.bar_theme[0].config

#         return bar.Bar(
#             widgets=self.widget,
#             size=bar_config.get("size", 24),
#             background=bar_config.get("background", "#cdd6f4"),
#             opacity=bar_config.get("opacity", 0.5),
#             margin=bar_config.get("margin", [0, 0, 0, 0]),
#             border_width=bar_config.get("border_width", 0),
#             border_color=bar_config.get("border_color", "#13CC0D"),
#         )


# widgets = WidgetManager().get_widget()


# def init_bar() -> bar.Bar:
#     return bar.Bar(
#         widgets=widgets,
#         size=24,
#         opacity=0.9,
#         background="#1a1a2e",
#     )
