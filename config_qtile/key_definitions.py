"""Определения клавиш для Qtile.

Модуль содержит:
- `KeyBinding`: датакласс для представления одной привязки клавиши;
- `KEYS_CONFIG`: список всех клавиатурных биндингов по умолчанию.

Каждый биндинг описывает действие, модификаторы, клавишу и команду Qtile.
"""

from dataclasses import dataclass

from constants import (
    BROWSER,
    EDITOR,
    FILE_MANAGER,
    FLAMESHOT_FULL,
    FLAMESHOT_GUI,
    POWER_MENU_SCRIPT,
    ROFI,
    YAZI,
)


@dataclass(frozen=True)
class KeyBinding:
    """Описание одной клавиатурной привязки для Qtile.

    Attrs:
        desc: Человекочитаемое описание действия.
        modifiers: Список модификаторов (например, `["mod"]`, `["mod", "shift"]`).
        key: Клавиша (например, `"h"`, `"Return"`, `"F12"`).
        command: Команда Qtile (например, `"layout.right"`, `"spawn"`).
        args: Дополнительные аргументы для команды (опционально).
    """

    desc: str
    modifiers: list[str]
    key: str
    command: str
    args: str | None = None


KEYS_CONFIG: list[KeyBinding] = [
    # Навигация
    KeyBinding("Фокус вправо", ["mod"], "l", "layout.right"),
    KeyBinding("Фокус влево", ["mod"], "h", "layout.left"),
    KeyBinding("Фокус вниз", ["mod"], "j", "layout.down"),
    KeyBinding("Фокус вверх", ["mod"], "k", "layout.up"),
    KeyBinding("Следующее окно", ["mod"], "w", "layout.next"),
    # Перемещение
    KeyBinding("Окно влево", ["mod", "shift"], "h", "layout.shuffle_left"),
    KeyBinding("Окно вправо", ["mod", "shift"], "l", "layout.shuffle_right"),
    KeyBinding("Окно вниз", ["mod", "shift"], "j", "layout.shuffle_down"),
    KeyBinding("Окно вверх", ["mod", "shift"], "k", "layout.shuffle_up"),
    # Размеры
    KeyBinding("Расширить влево", ["mod", "control"], "h", "layout.grow_left"),
    KeyBinding("Расширить вправо", ["mod", "control"], "l", "layout.grow_right"),
    KeyBinding("Расширить вниз", ["mod", "control"], "j", "layout.grow_down"),
    KeyBinding("Расширить вверх", ["mod", "control"], "k", "layout.grow_up"),
    KeyBinding("Сброс размеров", ["mod"], "n", "layout.normalize"),
    KeyBinding(
        "Смена раскладки",
        ["control", "shift"],
        "space",
        "widget.keyboardlayout.next_keyboard",
    ),
    # Layout
    KeyBinding("Следующий layout", ["mod"], "space", "next_layout"),
    # Окна
    KeyBinding("Закрыть окно", ["mod"], "q", "window.kill"),
    KeyBinding("Полный экран", ["mod"], "f", "window.toggle_fullscreen"),
    KeyBinding("Плавающее окно", ["mod"], "t", "window.toggle_floating"),
    # Система
    KeyBinding("Перезагрузка конфига", ["mod", "control"], "r", "reload_config"),
    KeyBinding("Выход", ["mod", "control"], "q", "shutdown"),
    KeyBinding("Запуск команды", ["mod"], "r", "spawncmd"),
    # Приложения
    KeyBinding("Терминал", ["mod"], "Return", "spawn", "{{terminal}}"),
    KeyBinding("Файловый менеджер", ["mod"], "e", "spawn", FILE_MANAGER),
    KeyBinding("VSCode", ["mod"], "c", "spawn", EDITOR),
    KeyBinding("Браузер", ["mod"], "b", "spawn", BROWSER),
    KeyBinding("Yazi", ["mod"], "z", "spawn", YAZI),
    KeyBinding("Rofi", ["mod"], "d", "spawn", ROFI),
    KeyBinding("Скриншот GUI", ["mod"], "o", "spawn", FLAMESHOT_GUI),
    KeyBinding(
        "Полноэкранная съемка (с запросом пути сохранения)n",
        ["mod", "shift"],
        "o",
        "spawn",
        FLAMESHOT_FULL,
    ),
    KeyBinding(
        "Power menu",
        [],
        "F12",
        "spawn",
        POWER_MENU_SCRIPT,
    ),
    # громкость
    KeyBinding(
        "Увеличение громкости",
        [],
        "XF86AudioRaiseVolume",
        "spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')",
    ),
    KeyBinding(
        "Уменьшение громкости",
        [],
        "XF86AudioLowerVolume",
        "spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')",
    ),
    KeyBinding(
        "Выключение громкости",
        [], "XF86AudioMute", "spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')",
    ),
]
