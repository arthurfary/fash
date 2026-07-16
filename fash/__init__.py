"""fash - build terminal user interfaces from a grid of widgets.

Quick start::

    from fash import Window, Drawer, TextWidget, Color

    window = Window(1, 2)
    window.set_at(0, 0, TextWidget("Left", "Hello", color=Color.RED))
    window.set_at(0, 1, TextWidget("Right", "World", color=Color.BLUE))

    Drawer(20, 80, window).draw_all()

To build a custom widget, subclass :class:`Widget` and return a
:class:`CellGrid` from ``draw``.
"""

from fash.core import (
    Cell,
    CellGrid,
    Color,
    CursorPositionError,
    InvalidCharacterLengthError,
    Style,
    Widget,
    WidgetOutOfBoundsError,
)
from fash.draw import Drawer
from fash.widgets import TextWidget, TextWidgetStyle
from fash.windowmanager import Window

__version__ = "0.1.0"

__all__ = [
    # Layout & rendering
    "Window",
    "Drawer",
    # Widgets
    "Widget",
    "TextWidget",
    "TextWidgetStyle",
    # Styling
    "Color",
    "Style",
    "Cell",
    "CellGrid",
    # Exceptions
    "InvalidCharacterLengthError",
    "CursorPositionError",
    "WidgetOutOfBoundsError",
    # Metadata
    "__version__",
]
