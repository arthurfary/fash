from abc import ABC, abstractmethod

from fash.core.cell_grid import CellGrid
from fash.core.keys import Key
from fash.core.signal import Signal


class Widget(ABC):
    """
    Widget class
    """

    @abstractmethod
    def draw(self, max_rows: int, max_cols: int) -> CellGrid:
        """
        Function that handles the displaying of the widget.

        Returns a formatted string, must be set between the bouderies of `max_height` and `max_height`
        """

    def handle_key(self, key: Key) -> Signal:
        """Return what should happen after this keypress: redraw, quit, both, or neither."""
        return Signal.NONE  # default: widgets that don't care about input just ignore keys

