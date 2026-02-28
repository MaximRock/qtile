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

THEME_COLOR = "catppuccin"  # "gruvbox" "c"

# kb = Keybindings(mod="mod1")
# keys: list = kb.get()

mod = "mod1"
terminal: str | None = guess_terminal()

keys = []
keys += create_keys(mod=mod, terminal=terminal)

groups: list[Group] = create_gpups(config_groups=work())
keys += create_group_keys(mod=mod, groups=groups)

tc = ThemeController(theme_color=THEME_COLOR)

lm = LayoutsManager(theme_controller=tc)
layouts = lm.get_layouts()

sm = ScreenManager(theme_controller=tc)

screens: list[Screen] = sm.get_screens()

# screens = create_screens(
#     theme_controller=tc
#     )

# qt = QtilePath()

# screens: list[Screen] = [
#     Screen(
#         top=BarManager(theme_controller=tc).init_bar(),
#         wallpaper=qt.get("walls/vodoem.jpeg"),
#         wallpaper_mode="center",
#     )
# ]

# theme = GruvboxTheme()
# layout_manager = LayoutManager()

# controller = ThemeController(
#     qtile=qtile,
#     layout_manager=layout_manager,
#     theme=theme,
# )

# layouts = layout_manager.build(theme)


# @hook.subscribe.startup_once
# def start() -> None:
#     Autostart().run()


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

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


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
