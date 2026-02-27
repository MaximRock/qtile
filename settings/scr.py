import json
from pathlib import Path

from libqtile.config import Screen

from settings.bar import BarManager
from settings.path import QtilePath
from settings.theme_controller import ThemeController


class ScreenManager:
    def __init__(
        self,
        theme_controller: ThemeController,
        config_file: str = "screen.json",
        walls_dir: str = "walls",
        wallpaper_ext: str = "jpeg",
    ) -> None:
        self.tc: ThemeController = theme_controller
        self.config_file: str = config_file
        self.walls_dir: str = walls_dir
        self.wallpaper_ext: str = wallpaper_ext
        self.qp: QtilePath = QtilePath()

        self._config: dict = {}
        self._screens = []

        self._load_config()
        self._create_screens()

    def _load_config(self) -> None:
        config_path: Path = self.qp.get(
            f"config_qtile/theme/settings_json/{self.config_file}"
        )

        try:
            with open(config_path, encoding="utf-8") as f:
                self._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ошибка загрузки: {e}")
            self._config = {}

    def _create_screens(self) -> None:
        bar_manager: BarManager = BarManager(theme_controller=self.tc)
        top_bar = bar_manager.init_bar()

        wallpaper_name = self._config.get("wallpaper", "vodoem")
        wallpaper_path = self.qp.get(f"{self.walls_dir}/{wallpaper_name}.{self.wallpaper_ext}")
        wallpaper_mode = self._config.get("wallpaper_mode", "center")

        self._screens: list[Screen] = [
            Screen(
                top=top_bar,
                wallpaper=str(wallpaper_path),
                wallpaper_mode=wallpaper_mode,
            )
        ]

    def get_screens(self) -> list[Screen]:
        return self._screens
