from libqtile.config import Group, Key
from libqtile.lazy import lazy


def create_keys(mod: str, terminal: str | None = None) -> list[Key]:
    """Настройка комбинаций клавиш"""

    keys: list[Key] = []

    def add(modifiers, key, commands, desc: str = "") -> None:
        """
        Добавить комбинацию клавиш.

        Args:
            modifiers: Модификатор или список модификаторов
            key: Клавиша
            command: Команда lazy
            desc: Описание (опционально)
        """
        if isinstance(modifiers, str):
            modifiers = [modifiers]
        keys.append(Key(modifiers, key, commands, desc=desc))

    # Окна
    add(mod, "l", lazy.layout.right(), "Фокус вправо")
    add(mod, "h", lazy.layout.left(), "Фокус влево")
    add(mod, "j", lazy.layout.down(), "Фокус вниз")
    add(mod, "k", lazy.layout.up(), "Фокус вверх")
    add(mod, "w", lazy.layout.next(), "Следующее окно")  # space

    # Перемещение окон
    add([mod, "shift"], "h", lazy.layout.shuffle_left(), "Окно влево")
    add([mod, "shift"], "l", lazy.layout.shuffle_right(), "Окно вправо")
    add([mod, "shift"], "j", lazy.layout.shuffle_down(), "Окно вниз")
    add([mod, "shift"], "k", lazy.layout.shuffle_up(), "Окно вверх")

    # Размеры окон
    add([mod, "control"], "h", lazy.layout.grow_left(), "Расширить влево")
    add(
        [mod, "control"], "l", lazy.layout.grow_right(), "Расширить вправо"
    )
    add([mod, "control"], "j", lazy.layout.grow_down(), "Расширить вниз")
    add([mod, "control"], "k", lazy.layout.grow_up(), "Расширить вверх")
    add(mod, "n", lazy.layout.normalize(), "Сброс размеров")

    # Запуск и управление
    add(
        ["control", "shift"],
        "space",
        lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Switch keyboard layout",
    )
    add(mod, "space", lazy.next_layout(), "Следующий layout")  # Tab
    add(mod, "Return", lazy.spawn(terminal), "Терминал")
    add(mod, "q", lazy.window.kill(), "Закрыть окно")
    add(mod, "f", lazy.window.toggle_fullscreen(), "Полный экран")
    add(mod, "t", lazy.window.toggle_floating(), "Плавающее окно")

    # Qtile
    add(
        [mod, "control"], "r", lazy.reload_config(), "Перезагрузка конфига"
    )
    add([mod, "control"], "q", lazy.shutdown(), "Выход из Qtile")
    add(mod, "r", lazy.spawncmd(), "Запуск команды")

    # apps
    add(mod, "e", lazy.spawn("thunar"), "Thunar Файловый менеджер")
    add(mod, "c", lazy.spawn("code"), "VsCode")
    add(mod, "z", lazy.spawn("wezterm start -- yazi"), "Yazi Терминальный менеджер")
    add(mod, "b", lazy.spawn("yandex-browser-stable"), "Яндекс браузер")

    # rofi
    add(mod, "d", lazy.spawn("rofi -show drun"), "запуск rofi")
    add(mod, "p", lazy.spawn("rofi -show power-menu"), "запуск rofi power-menu")

    # flameshot
    add(
        mod,
        "o",
        lazy.spawn("flameshot gui"),
        "захват с помощью графического интерфейса",
    )
    add(
        [mod, "shift"],
        "o",
        lazy.spawn("flameshot full"),
        "Полноэкранная съемка (с запросом пути сохранения)n",
    )

    add([], "F12", lazy.spawn("/home/max/.config/qtile/modules/power_menu/main.py")),

    return keys


def create_group_keys(mod: str, groups: list[Group]) -> list[Key]:
    keys_group: list[Key] = []

    for group in groups:
        keys_group.extend(
            [
                Key(
                    [mod],
                    group.name,
                    lazy.group[group.name].toscreen(),
                    desc=f"Переключиться на группу {group.name}",
                ),
                Key(
                    [mod, "shift"],
                    group.name,
                    lazy.window.togroup(group.name),
                    desc=f"Переместить окно в группу {group.name}",
                ),
            ]
        )

    return keys_group
