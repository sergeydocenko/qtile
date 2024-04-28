import os
import subprocess
import locale

from libqtile import layout, bar, widget, hook, qtile
from libqtile.lazy import lazy
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

locale.setlocale(locale.LC_TIME, "en_US")

colors = [
    ["#160B00", "#160B00"],  # background (dark grey) [0]
    ["#663300", "#663300"],  # darkorange [1]
    ["#8B4500", "#8B4500"],  # less dark orange (white) [2]
    ["#A35100", "#A35100"],  # less less dark orange [3]
    ["#C26100", "#C26100"],  # light orange [4]
    ["#E07000", "#E07000"],  # green [5]
    ["#FF7F00", "#FF7F00"],  # orange [6]
    ["#FF8E1F", "#FF8E1F"],  # pink [7]
    ["#FF8E1F", "#FF8E1F"],  # purple [8]
    ["#FF8E1F", "#FF8E1F"],  # red [9]
    ["#FF8E1F", "#FF8E1F"],
]  # yellow [10]

# backgroundColor = "#160B00"
# foregroundColor = "#DE7B1B"
# workspaceColor = "#DE7B1B"
# foregroundColorTwo = "#DE7B1B"

qtile_path = os.path.join(os.path.expanduser("~"), ".config", "qtile")

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


def Notfy(source, title, message):
    lazy.spawn(f'notify-send -a "{source}" "{title}" "{message}"')


# The keys will be here
keys = [
    # Qtile WM Control
    EzKey("C-A-r", lazy.restart()),
    EzKey("C-A-x", lazy.shutdown()),
    EzKey("C-A-c", lazy.reload_config()),
    # To test
    # KeyChord(
    #    [mod],
    #    "q",
    #    [
    #        EzKey("r", lazy.restart()),
    #        EzKey("x", lazy.shutdown()),
    #        EzKey("c", lazy.reload_config()),
    #        EzKey("t", lazy.spawn('notify-send -a "Huy" "Pizda" "Jigurda"')),
    #        EzKey("y", Notfy("Huy", "Pizda", "Jigutda")),
    #    ],
    # ),
    ## Window killing
    # EzKey("M-p", lazy.spawn('notify-send -a "Huy" "Pizda" "Jigurda"')),
    EzKey("M-x", lazy.window.kill()),
    # EzKey("M-S-x", lazy.spawn("xkill")),
    # Launchers
    # EzKey("M-<Return>", lazy.spawn("alacritty")),
    # EzKey("M-S-<Return>", lazy.spawn("dolphin")),
    # EzKey("M-<space>", lazy.spawn("rofi -show drun -show-icons")),
    # EzKey("M-S-<space>", lazy.spawn("rofi -show run -show-icons")),
    # EzKey("M-w", lazy.spawn("rofi -show window -show-icons")),
    # EzKey("<Print>", lazy.spawn("flameshot gui")),
    # EzKey("M-s", lazy.group["scratchpad"].dropdown_toggle("alacritty")),
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
    EzKey("M-f", lazy.window.toggle_floating()),
    EzKey("M-<Tab>", lazy.screen.toggle_group(), desc="Last active group"),
]

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            EzKey(f"M-{i.name}", lazy.group[i.name].toscreen()),
            EzKey(f"M-S-{i.name}", lazy.window.togroup(i.name, switch_group=True)),
        ]
    )

mouse = [
    EzDrag(
        "M-<Button1>",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    EzDrag(
        "M-<Button3>", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    EzClick("M-<Button2>", lazy.window.bring_to_front()),
]

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "#cc241d",
    "border_normal": "#555555",
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        new_client_position="bottom",
        single_border_width=0,
        single_margin=0,
    ),
    layout.Tile(**layout_theme),
    layout.Max(),
]

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=16,
    padding=3,
)

extension_defaults = widget_defaults.copy()


def sep():
    return widget.TextBox(text="•")


def top_bar_widgets():
    widgets = [
        # sep(),
        widget.GroupBox(highlight_method="block"),
        sep(),
        widget.CurrentLayout(),
        sep(),
        # widget.CurrentLayoutIcon(),
        # widget.PulseVolume(),
        widget.WindowName(),
        widget.Spacer(),
        widget.Systray(),
    ]
    return widgets


def bottom_bar_widgets():
    widgets = [
        # sep(),
        widget.LaunchBar(progs=[("", "firefox"), ("Code", "code")]),
        # sep(),
        widget.Spacer(),
        # sep(),
        widget.CPU(format=" {load_percent}%", update_interval=10),
        widget.CPUGraph(frequency=5),
        sep(),
        # widget.Memory(format="{MemUsed: .0f}{mm}", update_interval=5, measure_mem="G"),
        widget.Memory(
            format="{MemUsed: .0f}{mm}",
            update_interval=10,
            measure_mem="G",
            padding=0,
        ),
        widget.MemoryGraph(frequency=5),
        # sep(),
        # widget.HDDBusyGraph(fmt="{}", device="sda2", frequency=5),
        sep(),
        # widget.Net(
        #    interface="wlp3s0", format=" {down} {up}", update_interval=3, padding=5
        # ),
        # widget.NetGraph(
        #    interface="wlp3s0",
        #    frequency=5,
        # ),
        # sep(),
        widget.Clock(format="%Y-%m-%d %a %H:%M:%S"),
    ]
    return widgets


def init_screens():
    return [
        Screen(
            wallpaper=os.path.join(qtile_path, "media", "triangle.jpg"),
            wallpaper_mode="stretch",
            top=bar.Bar(widgets=top_bar_widgets(), size=24),
            bottom=bar.Bar(widgets=bottom_bar_widgets(), size=24),
        )
    ]


screens = init_screens()


floating_types = ["notification", "toolbar", "splash", "dialog", "popup"]


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


# @hook.subscribe.startup_once
# def start_apps():
#    qtile.cmd_spawn(["xrandr --output eDP-1 --primary --mode 1280x720"])
#    qtile.cmd_spawn(["dunst&"])
#    qtile.cmd_spawn(["nm-applet&"])
#    qtile.cmd_spawn(["pamac-tray&"])
#    qtile.cmd_spawn(["xfce4-power-manager&"])


# @hook.subscribe.startup_once
# def autostart():
#    once = os.path.expanduser("~/.config/qtile/scripts/autorun_once.sh")
#    subprocess.call([home])


@hook.subscribe.startup
def startup():
    startup = os.path.expanduser("~/.config/qtile/scripts/startup.sh")
    subprocess.call([startup])
