from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    config: dict = None

    def __post_init__(self) -> None:
        if self.config is None:
            self.config = {}


# from dataclasses import dataclass


# @dataclass
# class Theme:
#     # Основные цвета
#     name: str
#     background: str
#     foreground: str
#     accent: str
#     active: str
#     inactive: str

#     # layout параметры
#     border_width: int
#     border_focus: str
#     border_normal: str

#     # Bar
#     bar_height: int

#     # Widget
#     widget_background: str
#     widget_foreground: str
