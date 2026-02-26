from libqtile import layout
from settings.theme_controller import ThemeController
from settings.base_factory import BaseFactory


class LayoutsManager:
    def __init__(self, theme_controller: ThemeController = None) -> None:
        self.tc = theme_controller
        themes = self.tc.get_theme_layouts()
        colors = self.tc.get_theme_color()

        classes: dict[str, object] = {
            "Max": layout.Max,
            "Columns": layout.Columns,
            "Floating": layout.Floating,
            "Tile": layout.Tile,
            "Bsp": layout.Bsp,
        }

        fallback = [layout.Max()]
        self.factory = BaseFactory(
            themes=themes, classes=classes, fallback=fallback, colors=colors)

    def get_layouts(self):
        return self.factory.build()


    # def get_layouts(self):
    #     fallback = [layout.Max()]
    #     layouts = []

    #     for theme in self.themes:
    #         cls = self.classes.get(theme.name)
    #         if cls:
    #             layouts.append(cls(**theme.config))

    #     return layouts if layouts else fallback  # noqa: FURB110



# def get_layouts():
#     return [
#         layout.Spiral(
#             border_focus=theme.border_focus,
#             border_normal=theme.border_normal,
#             border_width=theme.border_width,
#         ),
#         layout.Columns(
#             border_focus=theme.border_focus,
#             border_normal=theme.border_normal,
#             border_width=theme.border_width,
#         ),
#     ]


# from libqtile import layout

# from config_qtile.theme.base import BaseTheme


# class LayoutManager:
#     def build(self, theme: BaseTheme):
#         return [layout.Columns(**theme.columns()),
#                 layout.Spiral(**theme.spiral())]
