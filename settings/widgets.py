from libqtile import widget

from config_qtile.theme.theme_model import Theme
from settings.base_factory import BaseFactory
from settings.theme_controller import ThemeController


class WidgetManager:
    def __init__(self, theme_controller: ThemeController = None) -> None:
        self.tc = theme_controller
        themes: list[Theme] = self.tc.get_theme_widgets()
        colors: dict = self.tc.get_theme_color()

        classes = {
            "GroupBox": widget.GroupBox,
            "Prompt": widget.Prompt,
            "CurrentLayout": widget.CurrentLayout,
            "Clock": widget.Clock,
            "keyboardlayout": widget.KeyboardLayout,
            "Spacer": widget.Spacer,
            "Systray": widget.Systray,
            "CPU": widget.CPU,
            "Memory": widget.Memory,
            "Net": widget.Net,
            "Volume": widget.Volume,
            "Battery": widget.Battery,
            "WindowName": widget.WindowName,
            "TextBox": widget.TextBox,
        }

        fallback = [
            widget.GroupBox(),
            widget.Prompt(),
            widget.CurrentLayout(),
            widget.Clock(format="%H:%M"),
        ]

        self.factory = BaseFactory(
            themes=themes, classes=classes, fallback=fallback, colors=colors
        )

    def get_widget(self):
        return self.factory.build()

    # def get_widget(self):
    #     fallback = [
    #         widget.GroupBox(),
    #         widget.Prompt(),
    #         widget.CurrentLayout(),
    #         widget.Clock(format="%H:%M"),
    #     ]

    #     widgets = []

    #     for item in self.themes:
    #         cls = self.classes.get(item.name)
    #         if cls:
    #             widgets.append(cls(**item.config))

    #     return widgets if widgets else fallback


# from libqtile import widget
# from config_qtile.theme.theme_model import Theme
# from settings.theme_controller import ThemeController

# theme: Theme = ThemeController().get_theme()


# def init_widgets():
#     return [
#         widget.CurrentLayout(),
#         widget.GroupBox(
#             background=theme.widget_background,
#             active=theme.active,
#             inactive=theme.inactive,
#             highlight_method="line",
#             this_current_screen_border=theme.border_focus,
#         ),
#         widget.Prompt(),
#         widget.Clock(
#             format="%Y-%m-%d %H:%M",
#             background=theme.widget_background,
#             foreground=theme.widget_foreground,
#         ),
#     ]
