# settings/screen.py

import json
from pathlib import Path

from libqtile.config import Screen

from settings.bar import BarManager
from settings.path import QtilePath
from settings.theme_controller import ThemeController


class ScreenManager:
    """
    Менеджер экранов для Qtile.

    Использует настройки из ThemeController для обоев и режимов.
    """

    def __init__(
        self,
        theme_controller: ThemeController,
        config_file: str = "screen.json",
        walls_dir: str = "walls",
    ) -> None:
        self.tc: ThemeController = theme_controller
        self.config_file: str = config_file
        self.walls_dir: str = walls_dir
        self.qp: QtilePath = QtilePath()

        # ✅ Получаем настройки из ThemeController
        self.settings: dict = self.tc.get_theme_settings()

        self._config: dict = {}
        self._screens: list[Screen] = []

        self._load_config()
        self._create_screens()

    def _load_config(self) -> None:
        """Загружает JSON конфигурацию экранов."""
        config_path: Path = self.qp.get(
            f"config_qtile/theme/settings_json/{self.config_file}"
        )

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
            print(f"Загружен конфиг экранов: {config_path}")
        except FileNotFoundError:
            print(f"Файл не найден: {config_path}")
            self._config = {}
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON в {config_path}: {e}")
            self._config = {}

    def _create_screens(self) -> None:
        """Создаёт объекты Screen с использованием настроек."""
        try:
            bar_manager: BarManager = BarManager(theme_controller=self.tc)
            top_bar = bar_manager.init_bar()

            # Обои: из конфига или из settings
            wallpaper_name = self._config.get(
                "wallpaper", self.settings.get("wallpaper", "vodoem")
            )

            # Расширение: из конфига или из settings
            wallpaper_ext = self._config.get(
                "wallpaper_ext", self.settings.get("wallpaper_ext", ".jpeg")
            )

            # Добавляем точку если нет
            if not wallpaper_ext.startswith("."):
                wallpaper_ext = f".{wallpaper_ext}"

            wallpaper_path: Path = self.qp.get(
                f"{self.walls_dir}/{wallpaper_name}{wallpaper_ext}"
            )

            # Режим: из конфига или из settings
            wallpaper_mode = self._config.get(
                "wallpaper_mode", self.settings.get("wallpaper_mode", "center")
            )

            self._screens = [
                Screen(
                    top=top_bar,
                    wallpaper=str(wallpaper_path),
                    wallpaper_mode=wallpaper_mode,
                )
            ]
            print(f"🖼️ Экран создан: {wallpaper_name}{wallpaper_ext} ({wallpaper_mode})")
        except Exception as e:
            print(f"❌ Ошибка создания экрана: {e}")
            self._screens = []

    def get_screens(self) -> list[Screen]:
        """Возвращает список экранов."""
        return self._screens

    def get_config(self) -> dict:
        """Возвращает текущую конфигурацию."""
        return self._config

    def reload(self) -> None:
        """Перезагружает конфигурацию и пересоздаёт экраны."""
        print("🔄 Перезагрузка экранов...")
        self._load_config()
        self._create_screens()
        print("✅ Экраны перезапущены")




# import json
# from pathlib import Path

# from libqtile.config import Screen

# from settings.bar import BarManager
# from settings.path import QtilePath
# from settings.theme_controller import ThemeController


# class ScreenManager:
#     def __init__(
#         self,
#         theme_controller: ThemeController,
#         config_file: str = "screen.json",
#         walls_dir: str = "walls",
#         wallpaper_ext: str = "jpeg",
#     ) -> None:
#         self.tc: ThemeController = theme_controller
#         self.config_file: str = config_file
#         self.walls_dir: str = walls_dir
#         self.wallpaper_ext: str = wallpaper_ext
#         self.qp: QtilePath = QtilePath()

#         self._config: dict = {}
#         self._screens = []

#         self._load_config()
#         self._create_screens()

#     def _load_config(self) -> None:
#         config_path: Path = self.qp.get(
#             f"config_qtile/theme/settings_json/{self.config_file}"
#         )

#         try:
#             with open(config_path, encoding="utf-8") as f:
#                 self._config = json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError) as e:
#             print(f"ошибка загрузки: {e}")
#             self._config = {}

#     def _create_screens(self) -> None:
#         bar_manager: BarManager = BarManager(theme_controller=self.tc)
#         top_bar = bar_manager.init_bar()

#         wallpaper_name = self._config.get("wallpaper", "vodoem")
#         wallpaper_path = self.qp.get(
#             f"{self.walls_dir}/{wallpaper_name}.{self.wallpaper_ext}"
#         )
#         wallpaper_mode = self._config.get("wallpaper_mode", "center")

#         self._screens: list[Screen] = [
#             Screen(
#                 top=top_bar,
#                 wallpaper=str(wallpaper_path),
#                 wallpaper_mode=wallpaper_mode,
#             )
#         ]

#     def get_screens(self) -> list[Screen]:
#         return self._screens


# def create_screens(
#         theme_controller: ThemeController,
#         config_file: str = "screen.json") -> list[Screen]:

#     qp: QtilePath = QtilePath()
#     config_path: Path = qp.get(f"config_qtile/theme/settings_json/{config_file}")

#     with open(config_path, encoding="utf-8") as f:
#         data = json.load(f)

#     bar_manager: BarManager = BarManager(theme_controller=theme_controller)
#     top_bar = bar_manager.init_bar()

#     screens: list[Screen] = [
#         Screen(
#             top=top_bar,
#             wallpaper=qp.get(f"walls/{data.get('wallpaper', 'vodoem')}.jpeg"),
#             wallpaper_mode=data.get("wallpaper_mode", "center"),
#         )
#     ]
#     return screens
