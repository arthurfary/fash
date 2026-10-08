"""Rendering: turn a window of widgets into terminal output.

:class:`Drawer` is the main entry point; :class:`Printer` is its low-level
output collaborator (kept separate so it can be substituted in tests). The
ANSI helpers remain internal.
"""

from fash.draw.drawer import Drawer
from fash.draw.printer import Printer

__all__ = [
    "Drawer",
    "Printer",
]