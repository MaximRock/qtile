

class BaseTheme:
    def __init__(
        self,
        border_focus: str,
        border_focus_stack: list[str],
        border_normal: str,
        border_width=2,
    ) -> None:
        self.border_focus: str = border_focus
        self.border_focus_stack: list[str] = border_focus_stack
        self.border_normal: str = border_normal
        self.border_width: int = border_width

    def _base_layout(self) -> dict[str, str | int | bool | list[str]]:
        return {
            "border_focus": self.border_focus,
            "border_focus_stack": self.border_focus_stack,
            "border_normal": self.border_normal,
            "border_width": self.border_width,
            "border_on_single": True,
        }

    def columns(self) -> dict[str, str | int | bool | list[str]]:
        return self._base_layout()

    def spiral(self) -> dict[str, str | int | bool | list[str]]:
        return self._base_layout()
