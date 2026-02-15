from libqtile.config import Key, Group
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



# from libqtile.config import Key
# from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal


# class Keybindings:
#     """Класс для управления комбинациями клавиш"""

#     def __init__(self, mod: str = "mod1") -> None:
#         """
#         Инициализация с модификатором.
#         Args:
#             mod: Основной модификатор (mod1 = Alt, mod4 = Win)
#         """
#         self.mod: str = mod
#         self.terminal = guess_terminal()
#         self.keys: list = []
#         self._setup_default()

#     def _setup_default(self) -> None:
#         """Настройка комбинаций клавиш"""
#         # Окна
#         self.add(self.mod, "h", lazy.layout.left(), "Фокус влево")
#         self.add(self.mod, "l", lazy.layout.right(), "Фокус вправо")
#         self.add(self.mod, "j", lazy.layout.down(), "Фокус вниз")
#         self.add(self.mod, "k", lazy.layout.up(), "Фокус вверх")
#         self.add(self.mod, "space", lazy.layout.next(), "Следующее окно")

#         # Перемещение окон
#         self.add([self.mod, "shift"], "h", lazy.layout.shuffle_left(), "Окно влево")
#         self.add([self.mod, "shift"], "l", lazy.layout.shuffle_right(), "Окно вправо")
#         self.add([self.mod, "shift"], "j", lazy.layout.shuffle_down(), "Окно вниз")
#         self.add([self.mod, "shift"], "k", lazy.layout.shuffle_up(), "Окно вверх")

#         # Размеры окон
#         self.add([self.mod, "control"], "h", lazy.layout.grow_left(), "Расширить влево")
#         self.add(
#             [self.mod, "control"], "l", lazy.layout.grow_right(), "Расширить вправо"
#         )
#         self.add([self.mod, "control"], "j", lazy.layout.grow_down(), "Расширить вниз")
#         self.add([self.mod, "control"], "k", lazy.layout.grow_up(), "Расширить вверх")
#         self.add(self.mod, "n", lazy.layout.normalize(), "Сброс размеров")

#         # Запуск и управление
#         self.add(self.mod, "Return", lazy.spawn(self.terminal), "Терминал")
#         self.add(self.mod, "Tab", lazy.next_layout(), "Следующий layout")
#         self.add(self.mod, "q", lazy.window.kill(), "Закрыть окно")
#         self.add(self.mod, "f", lazy.window.toggle_fullscreen(), "Полный экран")
#         self.add(self.mod, "t", lazy.window.toggle_floating(), "Плавающее окно")

#         # Qtile
#         self.add(
#             [self.mod, "control"], "r", lazy.reload_config(), "Перезагрузка конфига"
#         )
#         self.add([self.mod, "control"], "q", lazy.shutdown(), "Выход из Qtile")
#         self.add(self.mod, "r", lazy.spawncmd(), "Запуск команды")

#     def add(self, modifiers, key, commands, desc: str = "") -> None:
#         """
#         Добавить комбинацию клавиш.

#         Args:
#             modifiers: Модификатор или список модификаторов
#             key: Клавиша
#             command: Команда lazy
#             desc: Описание (опционально)
#         """
#         if isinstance(modifiers, str):
#             modifiers = [modifiers]

#         self.keys.append(Key(modifiers, key, commands, desc=desc))

#     def get(self) -> list:
#         return self.keys
