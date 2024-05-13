""" My Qtile Config """

import os
import subprocess
import locale
import webbrowser
import dataclasses
import re

from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.config import (
    EzDrag,
    EzKey,
    Group,
    Rule,
    Screen,
    ScratchPad,
    DropDown,
    Match,
)
from cs import ColorScheme

locale.setlocale(locale.LC_TIME, "ru_UA")

qtile_path = os.path.join(os.path.expanduser("~"), ".config", "qtile")

# pylint: disable=C0103
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = "focus"
wmname = "LG3D"
mod = "mod4"

colors = ColorScheme.Nord


@dataclasses.dataclass
class Env:
    """Environment settings"""

    Wlan = "wlp3s0"


modifier_keys = {
    "M": "mod4",
    "A": "mod1",
    "S": "shift",
    "C": "control",
    "T": "Tab",
}


def notfy(source, title, message):
    """Send onscreen notification"""
    lazy.spawn(f'notify-send -a "{source}" "{title}" "{message}"')


def kill_other_windows(qtile):
    """Kills all windows in the current group except the focused one."""
    group = qtile.current_group
    for window in group.windows:
        if window != qtile.current_window:
            window.kill()


# The keys will be here
keys = [
    # Qtile WM Control
    EzKey("C-A-r", lazy.restart()),
    EzKey("C-A-x", lazy.shutdown()),
    EzKey("C-A-c", lazy.reload_config()),
    # Close windows
    EzKey("M-x", lazy.window.kill()),
    EzKey("M-S-x", lazy.function(kill_other_windows)),
    #
    EzKey("M-<bracketleft>", lazy.screen.prev_group()),
    EzKey("M-<bracketright>", lazy.screen.next_group()),
    EzKey("M-S-<bracketleft>", lazy.prev_layout()),
    EzKey("M-S-<bracketright>", lazy.next_layout()),
    # Flip
    EzKey("M-f", lazy.layout.flip()),
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
    EzKey("M-C-m", lazy.layout.swap_main()),
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
    # EzKey("M-f", lazy.window.toggle_floating()),
    EzKey("M-<Tab>", lazy.screen.toggle_group(), desc="Last active group"),
    # Sratchpad
    EzKey("M-s", lazy.group["scratchpad"].dropdown_toggle("term")),
    EzKey("M-<grave>", lazy.group["scratchpad"].dropdown_toggle("grave")),
]

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


def CreateScratchpad(name, command):
    """Create named scratchpad with command"""
    return DropDown(
        name,
        command,
        height=0.9,
        width=0.9,
        y=0.05,
        x=0.05,
        warp_pointer=True,
    )


# Scratchpads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            CreateScratchpad(
                "grave",
                "alacritty -e tmux new-session -A -s 'grave'",
            ),
            CreateScratchpad(
                "term",
                "alacritty -e tmux new-session -A -s 'scratch'",
            ),
            CreateScratchpad(
                "htop_mem",
                "alacritty -e htop --sort-key=PERCENT_MEM",
            ),
            CreateScratchpad(
                "htop_cpu",
                "alacritty -e htop --sort-key=PERCENT_CPU",
            ),
            CreateScratchpad(
                "mtr",
                "alacritty -e mtr --displaymode 1 8.8.8.8",
            ),
            CreateScratchpad(
                "wavemon",
                "alacritty -e wavemon",
            ),
        ],
    )
)


dgroups_app_rules = [
    Rule(Match(wm_class=re.compile("^[Aa]udacious")), group="PLAYER"),
    # Rule(Match(wm_class=re.compile("[Navigator|firefox]")), group="1"),
    Rule(Match(wm_class=re.compile("^code-oss")), group="2"),
]

layout_theme = {
    "border_width": 5,
    "margin": 5,
    "border_focus": "#bf8b00",
    "border_normal": "#555555",
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        new_client_position="bottom",
        single_border_width=0,
        single_margin=0,
    ),
    layout.MonadWide(
        **layout_theme,
    ),
    # layout.Columns(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Bsp(**layout_theme),
    layout.Max(**layout_theme),
]

floating_layout = layout.Floating(**layout_theme)

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=20,
    padding=3,
    background="#0d1421",
)

extension_defaults = widget_defaults.copy()


def sep():
    """Predefined separator"""
    return widget.TextBox(text="•")


def spacer():
    """Predefined spacer"""
    return widget.Spacer(length=10)


def htop_cpu_handler():
    """Scratchpad with htop/cpu running"""
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("htop_cpu")}


def htop_mem_handler():
    """Scratchpad with htop/mem running"""
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("htop_mem")}


def wavemon_handler():
    """Scratchpad with htop/mem running"""
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("wavemon")}


def mtr_handler():
    """Scratchpad with mtr running"""
    return {
        "Button1": lazy.group["scratchpad"].dropdown_toggle("mtr"),
        "Button3": lazy.spawn(
            "echo qwe | sudo -e pkill NetworkManager && sleep 1s && sudo NetworkManager"
        ),
    }


def icon_locator(icon_name):
    """Locate icon in resouce folder"""
    return os.path.join(qtile_path, "assets", icon_name)


def top_bar_widgets():
    """Create top bar widgets"""
    widgets = [
        widget.GroupBox(highlight_method="block"),
        spacer(),
        widget.CurrentLayoutIcon(),
        # widget.CurrentLayout(fmt="{} "),
        spacer(),
        widget.WindowName(),
        spacer(),
        widget.Wttr(
            location={
                "kharkiv": "kharkiv",
            },
            format="%c %t %h",
            font="Hack Nerd Font",
            mouse_callbacks={
                "Button1": lambda: webbrowser.open("https://sinoptik.ua/погода-люботин")
            },
        ),
        spacer(),
        widget.WidgetBox(
            text_closed="[•]",
            text_opened="[>]",
            widgets=[
                widget.Clock(
                    background="#383748",
                    format="%Y-%m-%d %a",
                ),
            ],
        ),
        spacer(),
        widget.Clock(
            background="#383748",
            format="%H:%M",
        ),
        spacer(),
        widget.TextBox("[x]", mouse_callbacks={"Button1": lazy.window.kill()}),
    ]
    return widgets


def bottom_bar_widgets():
    """Create bottom bar widgets"""
    widgets = [
        widget.LaunchBar(
            progs=[
                (icon_locator("alacritty.png"), "alacritty"),
                (icon_locator("firefox.png"), "firefox"),
                (icon_locator("code.png"), "code"),
                (icon_locator("obsidian.png"), "obsidian"),
                (icon_locator("audacious.png"), "audacious -t"),
            ]
        ),
        widget.Spacer(),
        widget.WidgetBox(
            text_closed="[•]",
            # text_closed="[HEALTH]",
            text_opened="[>]",
            widgets=[
                widget.CPU(
                    format=" {load_percent}%",
                    update_interval=10,
                    mouse_callbacks=htop_cpu_handler(),
                ),
                widget.CPUGraph(
                    frequency=5,
                    mouse_callbacks=htop_cpu_handler(),
                ),
                widget.ThermalSensor(format="{temp:.0f}{unit}", threshold=85),
                spacer(),
                widget.Memory(
                    format="{MemUsed: .0f}{mm}",
                    update_interval=10,
                    measure_mem="G",
                    padding=0,
                    mouse_callbacks=htop_mem_handler(),
                ),
                widget.MemoryGraph(
                    frequency=5,
                    mouse_callbacks=htop_mem_handler(),
                ),
                spacer(),
                widget.Net(
                    interface=Env.Wlan,
                    prefix="M",
                    format="↓{down:.3f}{down_suffix} ↑{up:.3f}{up_suffix}",
                    mouse_callbacks=mtr_handler(),
                ),
                widget.NetGraph(
                    mouse_callbacks=mtr_handler(),
                ),
                widget.Wlan(
                    interface=Env.Wlan,
                    mouse_callbacks=wavemon_handler(),
                    format="{percent:2.0%}",
                ),
            ],
        ),
        spacer(),
        widget.Systray(
            background="#383748",
            padding=5,
        ),
    ]
    return widgets


def init_screens():
    """Create screen layout"""
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
    """Automatically sets window floating attribute for certain windows type"""
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


@hook.subscribe.startup
def startup():
    """Autorun script"""
    startup_script = os.path.expanduser("~/.config/qtile/scripts/startup.sh")
    subprocess.call([startup_script])
