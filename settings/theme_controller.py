

class ThemeController:
    def __init__(self, qtile, layout_manager, theme) -> None:
        self.qtile: object = qtile
        self.layout_manager: object = layout_manager
        self.theme: object = theme

    def apply(self) -> None:
        self.qtile.config.layouts = self.layout_manager.build(self.theme)
        self.qtile.cmd_reload_config()

    def set_theme(self, theme) -> None:
        self.theme = theme
        self.apply()
