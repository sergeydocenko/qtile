from libqtile import layout, bar, widget, hook
from libqtile.command import lazy
from libqtile.config import (
    EzClick,
    EzDrag,
    EzKey,
    Group,
    KeyChord,
    Screen,
    ScratchPad,
    DropDown,
    Match,
)
from modules.commands import Commands
from os import path
import os
import subprocess

qtile_path = path.join(path.expanduser("~"), ".config", "qtile")
commands = Commands()

main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = "smart"
wmname = "LG3D"
mod = "mod4"

modifier_keys = {
    "M": "mod4",
    "A": "mod1",
    "S": "shift",
    "C": "control",
    "T": "Tab",
}

# The keys will be here
keys = [
    # Qtile WM Control
    EzKey("C-A-r", lazy.restart()),
    EzKey("C-A-x", lazy.shutdown()),
    EzKey("C-A-c", lazy.reload_config()),

    # To test
    KeyChord([mod], "q", [
        EzKey("r", lazy.restart()),
        EzKey("x", lazy.shutdown()),
        EzKey('c', lazy.reload_config()),    
    ]),
    
    # Window killing
    EzKey("M-x", lazy.window.kill()),
    EzKey("M-S-x", lazy.spawn("xkill")),   

    # Launchers
    EzKey("M-<Return>",   lazy.spawn("alacritty")),
    EzKey("M-S-<Return>", lazy.spawn("dolphin")),
    EzKey("M-<space>",    lazy.spawn("rofi -show run -show-icons")),
    EzKey("M-S-<space>",  lazy.spawn("rofi -show drun -show-icons")),
    EzKey("M-<Tab>",      lazy.spawn("rofi -show window -show-icons")),
    EzKey("<Print>",      lazy.spawn("flameshot gui")),
    EzKey("M-s",          lazy.group["scratchpad"].dropdown_toggle("alacritty")),

    # Change layout
    EzKey("M-<bracketleft>", lazy.prev_layout()),
    EzKey("M-<bracketright>", lazy.next_layout()),

    # Switch between windows
    EzKey("M-h", lazy.layout.left()),
    EzKey("M-l", lazy.layout.right()),
    EzKey("M-j", lazy.layout.down()),
    EzKey("M-k", lazy.layout.up()), 

    # Move windows
    EzKey("M-C-h", lazy.layout.shuffle_left()),
    EzKey("M-C-l", lazy.layout.shuffle_right()),
    EzKey("M-C-j", lazy.layout.shuffle_down()),
    EzKey("M-C-k", lazy.layout.shuffle_up()),

    # Grow windows
    EzKey("M-S-h", lazy.layout.grow_left()),
    EzKey("M-S-l", lazy.layout.grow_right()),
    EzKey("M-S-j", lazy.layout.grow_down()),
    EzKey("M-S-k", lazy.layout.grow_up()),
    EzKey("M-S-n", lazy.layout.reset()),

    # Flip windows
    EzKey("M-A-h", lazy.layout.flip_left()),
    EzKey("M-A-l", lazy.layout.flip_right()),
    EzKey("M-A-j", lazy.layout.flip_down()),
    EzKey("M-A-k", lazy.layout.flip_up()),
    EzKey("M-n", lazy.layout.normalize()),

    EzKey("M-z", lazy.window.toggle_fullscreen(), desc="Zoom window"),
    EzKey("M-f", lazy.window.toggle_floating())
]

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        EzKey(f"M-{i.name}", lazy.group[i.name].toscreen()),
        EzKey(f"M-S-{i.name}", lazy.window.togroup(i.name, switch_group=True)),
    ])
    
mouse = [
    EzDrag(
        "M-<Button1>",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    EzDrag(
        "M-<Button3>", 
        lazy.window.set_size_floating(), 
        start=lazy.window.get_size()
    ),
    EzClick("M-<Button2>", lazy.window.bring_to_front()),
]

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "#cc241d",
    "border_normal": "#282828",
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        new_client_position="bottom",
        single_border_width=0,
        single_margin=0,
    ),
    layout.Tile(
        **layout_theme
    ),
    layout.Max(),
]

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=24,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Sep(padding=10),
                widget.CurrentLayout(),
                widget.Sep(padding=10),
                widget.Prompt(),
                widget.WindowName(),
            ],
            22,
        )
    ),
]


@hook.subscribe.startup
def autostart():
    autostart = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([autostart])


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == "dialog"
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True
