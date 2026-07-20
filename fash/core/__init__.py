"""Core building blocks: styling primitives, the widget base class and errors.

These are the pieces you need when creating your own widgets. Most users will
import from the top-level :mod:`fash` package instead of reaching in here.
"""

from fash.core.cell import Cell, Color, Style
from fash.core.cell_grid import CellGrid
from fash.core.exceptions import (
    CursorPositionError,
    InvalidCharacterLengthError,
    WidgetOutOfBoundsError,
)
from fash.core.widget import Widget

__all__ = [
    # Styling
    "Color",
    "Style",
    "Cell",
    # Widget authoring
    "Widget",
    "CellGrid",
    # Exceptions
    "InvalidCharacterLengthError",
    "CursorPositionError",
    "WidgetOutOfBoundsError",
]
