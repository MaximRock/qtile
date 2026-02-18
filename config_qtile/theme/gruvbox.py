from .base import BaseTheme


class GruvboxTheme(BaseTheme):
    def __init__(self) -> None:
        super().__init__(
            border_focus="#d79921",
            border_focus_stack=["#fabd2f", "#b57614"],
            border_normal="#282828",
            border_width=1
        )
