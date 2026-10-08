"""fash - build terminal user interfaces from a grid of widgets.

Structure and rendering come from :mod:`fash`; ready-made widgets live in
:mod:`fash.widgets`::

    from fash import App, Drawer, Signal, Window
    from fash.widgets import ListWidget

    def on_pick(item: str) -> Signal | None:
        return Signal.QUIT

    window = Window(1, 1)
    window.set_at(0, 0, ListWidget("Menu", "Pick one", ["alpha", "beta"], on_pick))

    App(Drawer(20, 60, window), focused_widget=window.get_at(0, 0)).run()

To build a custom widget, subclass :class:`fash.widgets.Widget` and return a
:class:`CellGrid` from ``draw``.
"""

from fash.app import App
from fash.core import (
    Cell,
    CellGrid,
    Color,
    CursorPositionError,
    InvalidCharacterLengthError,
    Style,
    WidgetOutOfBoundsError,
)
from fash.core.keys import Key, SpecialKey
from fash.core.signal import Signal
from fash.draw import Drawer
from fash.window import Window

__version__ = "0.1.0"

__all__ = [
    # Layout & rendering
    "Window",
    "Drawer",
    "App",
    # Styling
    "Color",
    "Style",
    "Cell",
    "CellGrid",
    # Input
    "Key",
    "SpecialKey",
    "Signal",
    # Exceptions
    "InvalidCharacterLengthError",
    "CursorPositionError",
    "WidgetOutOfBoundsError",
    # Metadata
    "__version__",
]
