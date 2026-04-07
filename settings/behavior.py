import json
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path

from settings.logger import get_logger
from settings.path import QtilePath

logger: Logger = get_logger("qtile.behavior", file="behavior")


@dataclass
class BehaviorConfig:
    path: str = ""

    # groups
    dgroups_key_binder: object = None
    dgroups_app_rules: list = field(default_factory=list)

    # focus
    follow_mouse_focus: bool = True
    bring_front_click: bool = False

    # windows
    floats_kept_above: bool = True
    cursor_warp: bool = False

    # behavior
    auto_fullscreen: bool = True
    focus_on_window_activation: str = "smart"
    focus_previous_on_window_remove: bool = False
    reconfigure_screens: bool = True
    auto_minimize: bool = True

    # wayland / cursor
    wl_input_rules: object = None
    wl_xcursor_theme: object = None
    wl_xcursor_size: int = 24

    # wm
    wmname: str = "LG3D"

    def __post_init__(self) -> None:
        self.qp: QtilePath = QtilePath()
        self.path: Path = Path(self.qp.get("config_qtile/settings_json/behavior.json"))
        data: dict = self._load_json(self.path)

        self._load_groups(data)
        self._load_focus(data)
        self._load_windows(data)
        self._load_behavior(data)
        self._load_wayland(data)
        self._load_wm(data)

    def _load_json(self, path: Path) -> dict:
        if not path.exists():
            logger.error(f"Файл не найден: {path}")
            raise FileNotFoundError(f"Файл не найден: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            logger.error("Конфигурационный файл должен быть JSON объектом")
            raise ValueError("Конфигурационный файл должен быть JSON объектом")

        return data

    def _get_bool(self, data: dict, key: str, default: bool) -> bool:
        value = data.get(key, default)
        if not isinstance(value, bool):
            logger.error(f"Значение '{key}' должно быть bool, получено: {type(value)}")
            raise ValueError(
                f"Значение '{key}' должно быть bool, получено: {type(value)}"
            )
        return value

    def _get_list(self, data: dict, key: str) -> list:
        value = data.get(key, [])
        if not isinstance(value, list):
            logger.error(f"Значение '{key}' должно быть list, получено: {type(value)}")
            raise ValueError(
                f"Значение '{key}' должно быть list, получено: {type(value)}"
            )
        return value

    def _get_str(self, data: dict, key: str, default: str) -> str:
        value = data.get(key, default)
        if not isinstance(value, str):
            logger.error(f"Значение '{key}' должно быть str, получено: {type(value)}")
            raise ValueError(
                f"Значение '{key}' должно быть str, получено: {type(value)}"
            )
        return value

    def _get_int(self, data: dict, key: str, default: int) -> int:
        value = data.get(key, default)
        if not isinstance(value, int):
            logger.error(f"Значение '{key}' должно быть int, получено: {type(value)}")
            raise ValueError(
                f"Значение '{key}' должно быть int, получено: {type(value)}"
            )
        return value

    def _load_groups(self, data: dict) -> None:
        self.dgroups_key_binder = data.get("dgroups_key_binder")
        self.dgroups_app_rules = self._get_list(data, "dgroups_app_rules")

    def _load_focus(self, data: dict) -> None:
        self.follow_mouse_focus = self._get_bool(data, "follow_mouse_focus", True)
        self.bring_front_click = self._get_bool(data, "bring_front_click", False)

    def _load_windows(self, data: dict) -> None:
        self.floats_kept_above = self._get_bool(data, "floats_kept_above", True)
        self.cursor_warp = self._get_bool(data, "cursor_warp", False)

    def _load_behavior(self, data: dict) -> None:
        self.auto_fullscreen = self._get_bool(data, "auto_fullscreen", True)
        self.focus_on_window_activation = self._get_str(
            data, "focus_on_window_activation", "smart"
        )
        self.focus_previous_on_window_remove = self._get_bool(
            data, "focus_previous_on_window_remove", False
        )
        self.reconfigure_screens = self._get_bool(data, "reconfigure_screens", True)
        self.auto_minimize = self._get_bool(data, "auto_minimize", True)

    def _load_wayland(self, data: dict) -> None:
        self.wl_input_rules = data.get("wl_input_rules", None)
        self.wl_xcursor_theme = data.get("wl_xcursor_theme", None)
        self.wl_xcursor_size = self._get_int(data, "wl_xcursor_size", 24)

    def _load_wm(self, data: dict) -> None:
        self.wmname = data.get("wmname", "LG3D")
