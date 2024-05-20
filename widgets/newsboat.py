""" Newsboat Widget """

import subprocess
import logging
from libqtile.widget import base

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Newsboat(base.ThreadPoolText):
    """ToggleClock Class"""

    defaults = [("update_interval", 60, "Check interval in seconds")]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(Newsboat.defaults)

    def poll(self):
        try:
            unread_count = (
                subprocess.check_output(["newsboat", "-x", "print-unread"])
                .decode("utf-8")
                .strip()
                .split()[0]
            )
            return unread_count
        except Exception as e:
            logger.warning("Error fetching Newsboat unread count: %s", e)
            return "N/A"
