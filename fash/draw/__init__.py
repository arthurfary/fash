"""Rendering: turn a window of widgets into terminal output.

:class:`Drawer` is the main entry point. :class:`Printer` and :class:`Reader`
are lower-level collaborators exposed mainly so they can be substituted (e.g.
in tests) via dependency injection. The ANSI helpers remain internal.
"""

from fash.draw.drawer import Drawer
from fash.draw.printer import Printer
from fash.draw.reader import Reader

__all__ = [
    "Drawer",
    "Printer",
    "Reader",
]
