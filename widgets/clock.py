""" Toggleable Format Clock Widget """

from libqtile import widget
from libqtile.lazy import lazy


class ToggleClock(widget.Clock):
    """ToggleClock Class"""

    def __init__(self, **config):
        super().__init__(**config)
        self.formats = ["%H:%M", "%H:%M:%S", "%Y-%m-%d %a %H:%M"]
        self.current_format = 0
        self.format = self.formats[self.current_format]
        self.mouse_callbacks = {"Button1": lazy.function(self.toggle_format)}

    def toggle_format(self, _):
        """Change format on click handler"""
        self.current_format = (self.current_format + 1) % len(self.formats)
        self.format = self.formats[self.current_format]
        self.tick()  # Force the clock to update immediately
