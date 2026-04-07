from logging import Logger
import os

import libqtile.resources
from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from config_qtile.config_groups import default, work
from settings.autostart import Autostart
from settings.bar import BarManager
from settings.groups import create_gpups
from settings.keys import create_group_keys, create_keys
from settings.layouts import LayoutsManager
from settings.theme_controller import ThemeController
from settings.screens import ScreenManager
from settings.behavior import BehaviorConfig
from settings.mouse import load_mouse
from settings.logger import get_logger
from constants import THEME_COLOR, MOD_KEY
from settings.key_manager import get_keys
from settings.floating import FloatingFactory


logger: Logger = get_logger("qtile.qtile_startup", file="qtile_startup")
logger.info("Qtile config started")


THEME_COLOR = THEME_COLOR  # "catppuccin" "gruvbox"

# kb = Keybindings(mod="mod1")
# keys: list = kb.get()

mod = MOD_KEY  # "mod1"
terminal: str | None = guess_terminal()

# keys: list = []
# keys += create_keys(mod=mod, terminal=terminal)
keys: list[Key] = get_keys(mod=mod, terminal=terminal)

groups: list[Group] = create_gpups(config_groups=work())
keys += create_group_keys(mod=mod, groups=groups)

tc = ThemeController(theme_color=THEME_COLOR)

lm = LayoutsManager(theme_controller=tc)
layouts: list = lm.get_layouts()

sm = ScreenManager(theme_controller=tc)

screens: list[Screen] = sm.get_screens()

mouse = load_mouse()


@hook.subscribe.startup_once
def autostart_apps() -> None:
    qtile.spawn(terminal)
    qtile.spawn("code")
    # qtile.cmd_spawn("Throne")


@hook.subscribe.startup_complete
def focus_terminal_group() -> None:
    qtile.groups_map["1"].toscreen()


for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

behavior = BehaviorConfig()
dgroups_key_binder: object = behavior.dgroups_key_binder
dgroups_app_rules: list = behavior.dgroups_app_rules
follow_mouse_focus: bool = behavior.follow_mouse_focus
bring_front_click: bool = behavior.bring_front_click
floats_kept_above: bool = behavior.floats_kept_above
cursor_warp: bool = behavior.cursor_warp

floating_config = FloatingFactory(tc).build()

floating_layout = floating_config.get_layout()

# fc = FloatingConfig()
# floating_layout = fc.get_floating_layout()

auto_fullscreen: bool = behavior.auto_fullscreen
focus_on_window_activation: str = behavior.focus_on_window_activation
focus_previous_on_window_remove: bool = behavior.focus_previous_on_window_remove
reconfigure_screens: bool = behavior.reconfigure_screens

auto_minimize: bool = behavior.auto_minimize

wl_input_rules: object = behavior.wl_input_rules
wl_xcursor_theme: object = behavior.wl_xcursor_theme
wl_xcursor_size: int = behavior.wl_xcursor_size

wmname: str = behavior.wmname


# groups = [Group(i) for i in "123456789"]

# for i in groups:
#     keys.extend(
#         [
#             # mod + group number = switch to group
#             Key(
#                 [kb.mod],
#                 i.name,
#                 lazy.group[i.name].toscreen(),
#                 desc=f"Switch to group {i.name}",
#             ),
#             # mod + shift + group number = switch to & move focused window to group
#             Key(
#                 [kb.mod, "shift"],
#                 i.name,
#                 lazy.window.togroup(i.name, switch_group=True),
#                 desc=f"Switch to & move focused window to group {i.name}",
#             ),
#             # Or, use below if you prefer not to switch to that group.
#             # # mod + shift + group number = move focused window to group
#             # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#             #     desc="move focused window to group {}".format(i.name)),
#         ]
#     )

# layouts = [
#     layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
#     layout.Max(),
#     # Try more layouts by unleashing below layouts.
#     # layout.Stack(num_stacks=2),
#     # layout.Bsp(),
#     # layout.Matrix(),
#     # layout.MonadTall(),
#     # layout.MonadWide(),
#     # layout.RatioTile(),
#     # layout.Tile(),
#     # layout.TreeTab(),
#     # layout.VerticalTile(),
#     # layout.Zoomy(),
# ]
# widget_defaults = dict(
#     font="sans",
#     fontsize=12,
#     padding=3,
# )
# extension_defaults = widget_defaults.copy()

# logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
# screens = [
#     Screen(
#         bottom=bar.Bar(
#             [
#                 widget.CurrentLayout(),
#                 widget.GroupBox(),
#                 widget.Prompt(),
#                 widget.WindowName(),
#                 widget.Chord(
#                     chords_colors={
#                         "launch": ("#ff0000", "#ffffff"),
#                     },
#                     name_transform=lambda name: name.upper(),
#                 ),
#                 widget.TextBox("default config", name="default"),
#                 widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                 # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
#                 # widget.StatusNotifier(),
#                 widget.Systray(),
#                 widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
#                 widget.QuickExit(),
#             ],
#             24,
#             # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
#             # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
#         ),
#         background="#000000",
#         # wallpaper=logo,
#         # wallpaper_mode="center",
#         # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
#         # By default we handle these events delayed to already improve performance, however your system might still be struggling
#         # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
#         # x11_drag_polling_rate = 60,
#     ),
# ]


# # Drag floating layouts.
# mouse = [
#     Drag(
#         [mod],
#         "Button1",
#         lazy.window.set_position_floating(),
#         start=lazy.window.get_position(),
#     ),
#     Drag(
#         [mod],
#         "Button3",
#         lazy.window.set_size_floating(),
#         start=lazy.window.get_size(),
#     ),
#     Click([mod], "Button2", lazy.window.bring_to_front()),
# ]

# dgroups_key_binder = None
# dgroups_app_rules = []  # type: list
# follow_mouse_focus = True
# bring_front_click = False
# floats_kept_above = True
# cursor_warp = False
# floating_layout = layout.Floating(
#     float_rules=[
#         # Run the utility of `xprop` to see the wm class and name of an X client.
#         *layout.Floating.default_float_rules,
#         Match(wm_class="confirmreset"),  # gitk
#         Match(wm_class="makebranch"),  # gitk
#         Match(wm_class="maketag"),  # gitk
#         Match(wm_class="ssh-askpass"),  # ssh-askpass
#         Match(title="branchdialog"),  # gitk
#         Match(title="pinentry"),  # GPG key password entry
#         Match(title="tk"),
#     ]
# )