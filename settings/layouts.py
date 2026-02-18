from libqtile import layout
from config_qtile.theme.base import BaseTheme


class LayoutManager:
    def build(self, theme: BaseTheme):
        return [layout.Columns(**theme.columns()),
                layout.Spiral(**theme.spiral())]
