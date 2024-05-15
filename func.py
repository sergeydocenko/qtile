""" Misc handy functions """

from libqtile.lazy import lazy


def notfy(source, title, message):
    """Send onscreen notification"""
    lazy.spawn(f'notify-send -a "{source}" "{title}" "{message}"')


def kill_other_windows(qtile):
    """Kills all windows in the current group except the focused one."""
    group = qtile.current_group
    for window in group.windows:
        if window != qtile.current_window:
            window.kill()


def kill_all_windows(qtile):
    """Kills all windows in the current group."""
    group = qtile.current_group
    for window in group.windows:
        window.kill()


def switch_to_urgent_group(qtile):
    """Switch to group where application set urgency flag"""
    for group in qtile.groups:
        if any(w.urgent for w in group.windows):
            group.cmd_toscreen()
            for w in group.windows:
                if w.urgent:
                    group.focus(w)
                    break
            break
