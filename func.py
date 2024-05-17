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


def swap_group_content(qtile, direction):
    """Move groups all around"""
    current_group = qtile.current_group
    current_group_idx = qtile.groups.index(current_group)

    if direction == 1:
        target_group_idx = (current_group_idx + 1) % len(qtile.groups)
    elif direction == -1:
        target_group_idx = (current_group_idx - 1) % len(qtile.groups)

    target_group = qtile.groups[target_group_idx]

    # Get windows in current and target groups
    current_windows = current_group.windows.copy()
    target_windows = target_group.windows.copy()

    # Remove windows from current and target groups
    for window in current_windows:
        window.togroup(target_group.name, switch_group=False)
    for window in target_windows:
        window.togroup(current_group.name, switch_group=False)

    # Optionally, switch to the target group
    qtile.groups[target_group_idx].cmd_toscreen()
