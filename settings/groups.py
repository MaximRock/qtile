from libqtile.config import Group, Key, Match
from libqtile.lazy import lazy


def create_gpups(config_groups: list[dict]) -> list[Group]:
    groups = [Group(**group) for group in config_groups]
    return groups



# class GroupManager:
#     """
#     Класс для управления группами
#     """
#     def __init__(self, mod: str, keys: list) -> None:
#         """
#         Args:
#             mod: Модификатор (mod1 или mod4)
#             keys: Список клавиш из Keybindings (изменяется in-place)
#         """
#         self.mod: str = mod
#         self.keys: list = keys
#         self.groups: list[Group] = []

#     def setup_groups_layouts(self) -> list[Group]:
#         """Создать группы"""
#         return [
#                 Group("1", matches=[Match(wm_class="wezterm")]),
#                 Group("2", matches=[Match(wm_class="code")]),
#                 Group("3"),
#                 Group("4"),
#                 Group("5"),
#                 Group("6"),
#                 Group("7"),
#                 Group("8"),
#                 Group("9"),
#                 ]

#     def setup(self) -> None:
#         """Настроить группы и клавиши."""
#         self.groups = self.setup_groups_layouts()

#         for group in self.groups:
#             self.keys.extend(
#                 [
#                     Key([self.mod], group.name, lazy.group[group.name].toscreen()),
#                     Key(
#                         [self.mod, "shift"], group.name, lazy.window.togroup(group.name)
#                     ),
#                 ]
#             )
