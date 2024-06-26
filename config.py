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
    Key,
    KeyChord,
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
from func import (
    kill_all_windows,
    kill_other_windows,
    switch_to_urgent_group,
    swap_group_content,
)
from widgets.clock import ToggleClock

locale.setlocale(locale.LC_TIME, "ru_UA")


class Paths:
    """Important path"""

    qtile = os.path.join(os.path.expanduser("~"), ".config", "qtile")
    tools = os.path.join(qtile, "configs")
    assets = os.path.join(qtile, "assets")
    wallpapers = os.path.join(qtile, "wallpapers")
    tmux_config = os.path.join(tools, "tmux", "tmux.conf")
    scripts = os.path.join(qtile, "scripts")


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


# The keys will be here
keys = [
    # Qtile WM Control
    EzKey("C-A-r", lazy.restart()),
    EzKey("C-A-x", lazy.shutdown()),
    EzKey("C-A-c", lazy.reload_config()),
    # Close windows
    EzKey("M-x", lazy.window.kill()),
    EzKey("M-S-x", lazy.function(kill_other_windows)),
    EzKey("M-C-x", lazy.function(kill_all_windows)),
    #
    EzKey("M-<bracketleft>", lazy.screen.prev_group()),
    EzKey("M-<bracketright>", lazy.screen.next_group()),
    #
    EzKey("M-C-<bracketleft>", lazy.function(swap_group_content, direction=-1)),
    EzKey("M-C-<bracketright>", lazy.function(swap_group_content, direction=1)),
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
    # Resuze windows
    EzKey(
        "M-S-h",
        lazy.layout.shrink_main().when(layout="monadtall"),
    ),
    EzKey(
        "M-S-j",
        lazy.layout.grow_main().when(layout="monadwide"),
    ),
    EzKey(
        "M-S-k",
        lazy.layout.shrink_main().when(layout="monadwide"),
    ),
    EzKey(
        "M-S-l",
        lazy.layout.grow_main().when(layout="monadtall"),
    ),
    # Flip windows
    EzKey("M-A-h", lazy.layout.flip_left()),
    EzKey("M-A-l", lazy.layout.flip_right()),
    EzKey("M-A-j", lazy.layout.flip_down()),
    EzKey("M-A-k", lazy.layout.flip_up()),
    # Additional control
    EzKey("M-S-n", lazy.layout.reset()),
    EzKey("M-n", lazy.layout.normalize()),
    EzKey("M-z", lazy.window.toggle_fullscreen(), desc="Zoom window"),
    EzKey("M-u", lazy.function(switch_to_urgent_group)),
    # EzKey("M-f", lazy.window.toggle_floating()),
    EzKey("M-<Tab>", lazy.screen.toggle_group(), desc="Last active group"),
    # Sratchpads
    EzKey("M-<grave>", lazy.group["scratchpad"].dropdown_toggle("grave")),
    EzKey("M-s", lazy.group["scratchpad"].dropdown_toggle("scratch")),
    EzKey("M-a", lazy.group["scratchpad"].dropdown_toggle("audacious")),
    #
    KeyChord(
        [mod],
        "o",
        [
            Key([], "n", lazy.group["scratchpad"].dropdown_toggle("newsboat")),
            Key([], "c", lazy.group["scratchpad"].dropdown_toggle("htop_cpu")),
            Key([], "m", lazy.group["scratchpad"].dropdown_toggle("htop_mem")),
            Key([], "w", lazy.group["scratchpad"].dropdown_toggle("wavemon")),
            Key([], "t", lazy.group["scratchpad"].dropdown_toggle("mtr")),
        ],
        name="[n]-News [c]-Cpu [m]-Memory [w]-WaveMon [t]-Mtr",
    ),
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


def CreateScratchpad(name, command, height=0.9, width=0.9):
    """Create named scratchpad with command"""
    return DropDown(
        name,
        command,
        height=height,
        width=width,
        y=(1 - height) / 2,
        x=(1 - width) / 2,
        warp_pointer=True,
    )


# Scratchpads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            CreateScratchpad(
                "grave",
                f"alacritty -e tmux -f '{Paths.tmux_config}' new-session -A -s 'grave'",
            ),
            CreateScratchpad(
                "scratch",
                f"alacritty -e tmux -f '{Paths.tmux_config}' new-session -A -s 'scratch'",
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
            CreateScratchpad(
                "newsboat",
                f"alacritty -e tmux -f '{Paths.tmux_config}' new-session -A -s 'newsboat' 'newsboat'",
            ),
            CreateScratchpad(
                "audacious",
                "audacious",
            ),
        ],
    )
)


dgroups_app_rules = [
    # Rule(Match(wm_class=re.compile("^[Aa]udacious")), group="PLAYER"),
    # Rule(Match(wm_class=re.compile("[Navigator|firefox]")), group="1"),
    Rule(Match(wm_class=re.compile("^code-oss")), group="2"),
]

layout_theme = {
    "border_width": 3,
    "margin": 7,
    "border_focus": "#bf8b00",
    "border_normal": "#666666",
    "single_border_width": 0,
    "single_margin": 0,
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        ratio=0.6,
    ),
    layout.MonadWide(
        **layout_theme,
        ratio=0.6,
    ),
    # layout.RatioTile(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Max(**layout_theme),
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


def newsboat_handler():
    """Scratchpad with newsboat running"""
    return {"Button1": lazy.group["scratchpad"].dropdown_toggle("newsboat")}


def mtr_handler():
    """Scratchpad with mtr running"""
    return {
        "Button1": lazy.group["scratchpad"].dropdown_toggle("mtr"),
        "Button3": lazy.spawn(
            "echo qwe | sudo -e pkill NetworkManager && sleep 1s && sudo NetworkManager"
        ),
    }


def icon_locator(icon_name):
    """
    Locate icon in resouce folder
    return $QTILE/assets/icon_name
    """
    return os.path.join(Paths.assets, icon_name)


widget_background_accent = "#302f45"


def top_bar_widgets():
    """Create top bar widgets"""
    widgets = [
        widget.GroupBox(
            highlight_method="block",
            disable_drag=True,
            rounded=True,
            # background=widget_background_accent,
        ),
        spacer(),
        widget.CurrentLayoutIcon(),
        spacer(),
        widget.WindowName(
            # background=widget_background_accent,
        ),
        spacer(),
        widget.OpenWeather(
            location="Kharkiv",
            metric=True,
            format="{icon}{main_temp:.0f}°{units_temperature} {wind_speed:.1f}m/s {wind_direction}",
            update_interval=600,
            background=widget_background_accent,
            mouse_callbacks={
                "Button1": lambda: webbrowser.open("https://sinoptik.ua/погода-люботин")
            },
        ),
        spacer(),
        ToggleClock(
            background=widget_background_accent,
        ),
        spacer(),
        widget.TextBox(
            "[<b>x</b>]",
            background=widget_background_accent,
            mouse_callbacks={"Button1": lazy.window.kill()},
        ),
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
            ],
            background=widget_background_accent,
        ),
        widget.Spacer(),
        widget.WidgetBox(
            text_closed="[•]",
            text_opened="[>]",
            background=widget_background_accent,
            widgets=[
                spacer(),
                widget.CPU(
                    format=" {load_percent}%",
                    update_interval=10,
                    mouse_callbacks=htop_cpu_handler(),
                    background=widget_background_accent,
                ),
                widget.CPUGraph(
                    frequency=5,
                    mouse_callbacks=htop_cpu_handler(),
                    background=widget_background_accent,
                ),
                widget.ThermalSensor(
                    format="{temp:.0f}{unit}",
                    threshold=85,
                    background=widget_background_accent,
                ),
                spacer(),
                widget.Memory(
                    format="{MemUsed: .0f}{mm}{MemPercent: .0f}%",
                    update_interval=10,
                    measure_mem="G",
                    padding=0,
                    mouse_callbacks=htop_mem_handler(),
                    background=widget_background_accent,
                ),
                widget.MemoryGraph(
                    frequency=5,
                    mouse_callbacks=htop_mem_handler(),
                    background=widget_background_accent,
                ),
                spacer(),
                widget.Net(
                    interface=Env.Wlan,
                    prefix="M",
                    format="  ↓{down:0.3f}{down_suffix} ↑{up:0.3f}{up_suffix}",
                    mouse_callbacks=mtr_handler(),
                    background=widget_background_accent,
                ),
                widget.NetGraph(
                    mouse_callbacks=mtr_handler(),
                ),
                widget.Wlan(
                    interface=Env.Wlan,
                    mouse_callbacks=wavemon_handler(),
                    format="{percent:2.0%}",
                    background=widget_background_accent,
                ),
            ],
        ),
        spacer(),
        widget.Systray(
            icon_size=20,
            padding=5,
            background=widget_background_accent,
        ),
        spacer(),
        widget.TextBox(
            "[<b>N</b>]",
            background=widget_background_accent,
            mouse_callbacks={
                "Button1": lambda: subprocess.call(
                    os.path.join(Paths.scripts, "nmrestart.sh")
                )
            },
        ),
    ]
    return widgets


def init_screens():
    """Create screen layout"""
    return [
        Screen(
            wallpaper=os.path.join(Paths.wallpapers, "hexes.jpg"),
            wallpaper_mode="stretch",
            top=bar.Bar(widgets=top_bar_widgets(), size=24),
            bottom=bar.Bar(widgets=bottom_bar_widgets(), size=24),
        )
    ]


screens = init_screens()


@hook.subscribe.client_new
def set_floating(window):
    """Automatically sets window floating attribute for certain windows type"""
    floating_types = ["notification", "toolbar", "splash", "dialog", "popup"]
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
