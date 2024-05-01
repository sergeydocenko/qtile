import os
import subprocess
import locale
import webbrowser

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

locale.setlocale(locale.LC_TIME, "ru_UA")

from cs import ColorScheme

colors = ColorScheme.Nord

# colors = [
#    ["#160B00", "#160B00"],  # background (dark grey) [0]
#    ["#663300", "#663300"],  # darkorange [1]
#    ["#8B4500", "#8B4500"],  # less dark orange (white) [2]
#    ["#A35100", "#A35100"],  # less less dark orange [3]
#    ["#C26100", "#C26100"],  # light orange [4]
#    ["#E07000", "#E07000"],  # green [5]
#    ["#FF7F00", "#FF7F00"],  # orange [6]
#    ["#FF8E1F", "#FF8E1F"],  # pink [7]
#    ["#FF8E1F", "#FF8E1F"],  # purple [8]
#    ["#FF8E1F", "#FF8E1F"],  # red [9]
#    ["#FF8E1F", "#FF8E1F"],  # yellow [10]

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

myTerm = "alacritty"

modifier_keys = {
    "M": "mod4",
    "A": "mod1",
    "S": "shift",
    "C": "control",
    "T": "Tab",
}


def Notfy(source, title, message):
    lazy.spawn(f'notify-send -a "{source}" "{title}" "{message}"')


@lazy.function
def kill_other_windows(qtile):
    """Kills all windows in the current group except the focused one."""
    current_window = qtile.currentWindow
    if current_window is not None:
        for window in qtile.currentGroup.windows:
            if window != current_window:
                window.kill()


@lazy.function
def kill_other_windows_in_group(qtile):
    Notfy("Pizda", "dfgs", "asdfasfd")
    focused_win_id = qtile.currentWindow
    group_name = qtile.current_group.name
    for window in qtile.windows_map[group_name]:
        if window != focused_win_id:
            window.kill()


# The keys will be here
keys = [
    # Qtile WM Control
    EzKey("C-A-r", lazy.restart()),
    EzKey("C-A-x", lazy.shutdown()),
    EzKey("C-A-c", lazy.reload_config()),
    EzKey("M-x", lazy.window.kill()),
    EzKey("M-d", kill_other_windows_in_group()),  # TODO: implement!!!
    # EzKey("M-r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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
    EzKey(
        "M-S-h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    EzKey(
        "M-S-l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    EzKey(
        "M-S-j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    EzKey(
        "M-S-k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    # Reset layout
    EzKey("M-S-n", lazy.layout.reset()),
    # Flip windows
    EzKey("M-A-h", lazy.layout.flip_left()),
    EzKey("M-A-l", lazy.layout.flip_right()),
    EzKey("M-A-j", lazy.layout.flip_down()),
    EzKey("M-A-k", lazy.layout.flip_up()),
    # Additional control
    EzKey("M-n", lazy.layout.normalize()),
    EzKey("M-z", lazy.window.toggle_fullscreen(), desc="Zoom window"),
    EzKey("M-f", lazy.window.toggle_floating()),
    EzKey("M-<Tab>", lazy.screen.toggle_group(), desc="Last active group"),
]

# Create groups
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            EzKey(f"M-{i.name}", lazy.group[i.name].toscreen()),
            EzKey(f"M-S-{i.name}", lazy.window.togroup(i.name, switch_group=True)),
        ]
    )

# Scratchpads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                "alacritty -e tmux new-session -A -s 'scratchpad'",
                height=0.9,
                width=0.9,
                y=0.05,
                x=0.05,
                warp_pointer=True,
            ),
            DropDown(
                "htop_mem",
                "alacritty -e htop --sort-key=PERCENT_MEM",
                height=0.9,
                width=0.9,
                y=0.05,
                x=0.05,
                warp_pointer=True,
            ),
            DropDown(
                "htop_cpu",
                "alacritty -e htop --sort-key=PERCENT_CPU",
                height=0.9,
                width=0.9,
                y=0.05,
                x=0.05,
                warp_pointer=True,
            ),
            DropDown(
                "mtr",
                "alacritty -e mtr --displaymode 1 8.8.8.8",
                height=0.9,
                width=0.9,
                y=0.05,
                x=0.05,
                warp_pointer=True,
            ),
            DropDown(
                "calendar",
                "alacritty -e cal",
                height=0.9,
                width=0.9,
                y=0.05,
                x=0.05,
                warp_pointer=True,
            ),
        ],
    )
)

keys.extend([EzKey("M-s", lazy.group["scratchpad"].dropdown_toggle("term"))])

# Mouse settings
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
    # layout.Bsp(**layout_theme),
    layout.Max(),
]

widget_defaults = dict(
    font="Source Code Pro",
    # fontsize=16,
    fontsize=20,
    padding=3,
)

extension_defaults = widget_defaults.copy()


def sep():
    return widget.TextBox(text="•")


def spacer():
    return widget.Spacer(length=15)


def htop_cpu_handler():
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("htop_cpu")}


def htop_mem_handler():
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("htop_mem")}


def mtr_handler():
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("mtr")}


def icon_locator(IconName):
    """Locate icon in resouce folder"""
    return os.path.join(qtile_path, "assets", IconName)


def top_bar_widgets():
    widgets = [
        widget.GroupBox(highlight_method="block"),
        spacer(),
        widget.CurrentLayoutIcon(),
        spacer(),
        widget.WindowName(),
        spacer(),
        widget.Wttr(
            location={
                "kharkiv": "kharkiv",
            },
            format="%c %t %h",
            font="Hack Nerd Font",
            background="#383748",
            mouse_callbacks={
                "Button1": lambda: webbrowser.open(
                    "https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BB%D1%8E%D0%B1%D0%BE%D1%82%D0%B8%D0%BD"
                )
            },
        ),
        spacer(),
        widget.Clock(
            # TODO: Copy date-time to clipboard on click
            format="%Y-%m-%d %a %H:%M",
            background="#383748",
        ),
    ]
    return widgets


# lazy.spawn(f'notify-send -a "{source}" "{title}" "{message}"')


def bottom_bar_widgets():
    widgets = [
        widget.TextBox(
            "XKill",
            # mouse_callbacks={"Button1": lazy.spawn("xkill")},
            mouse_callbacks={"Button1": lazy.spawn("xkill&")},
        ),
        # widget.TextBox(
        #    "Kill",
        #    mouse_callbacks={
        #        "Button1": lambda: subprocess.run(
        #            "sh -e 'echo qwe | sudo -S systemctl restart NetworkManager.service'"
        #        )
        #    },
        # ),
        widget.LaunchBar(
            progs=[
                (icon_locator("alacritty.png"), "alacritty"),
                (icon_locator("firefox.png"), "firefox"),
                (icon_locator("code.png"), "code"),
                (icon_locator("audacious.png"), "audacious -t"),
            ]
        ),
        widget.Spacer(),
        widget.CPU(
            format=" {load_percent}%",
            update_interval=10,
            mouse_callbacks=htop_cpu_handler(),
            background="#383748",
        ),
        widget.CPUGraph(
            frequency=5,
            mouse_callbacks=htop_cpu_handler(),
            background="#383748",
        ),
        spacer(),
        widget.Memory(
            format="{MemUsed: .0f}{mm}",
            update_interval=10,
            measure_mem="G",
            padding=0,
            mouse_callbacks=htop_mem_handler(),
            background="#383748",
        ),
        widget.MemoryGraph(
            frequency=5,
            mouse_callbacks=htop_mem_handler(),
            background="#383748",
        ),
        spacer(),
        widget.Net(
            interface="wlp3s0",
            prefix="M",
            format="↓{down:.3f}{down_suffix} ↑{up:.3f}{up_suffix}",
            mouse_callbacks=mtr_handler(),
            background="#383748",
        ),
        widget.NetGraph(
            background="#383748",
            mouse_callbacks=mtr_handler(),
        ),
        spacer(),
        widget.Systray(
            background="#383748",
            padding=5,
        ),
    ]
    return widgets


def init_screens():
    return [
        Screen(
            wallpaper=os.path.join(qtile_path, "assets", "triangle.jpg"),
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


@hook.subscribe.startup
def startup():
    startup = os.path.expanduser("~/.config/qtile/scripts/startup.sh")
    subprocess.call([startup])
