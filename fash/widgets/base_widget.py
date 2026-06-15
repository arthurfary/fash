from abc import ABC, abstractmethod

from fash.core.cell_grid import CellGrid


class Widget(ABC):
    """
    Widget class
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self, max_rows: int, max_cols: int) -> CellGrid:
        """
        Function that handles the displaying of the widget.

        Returns a formatted string, must be set between the bouderies of `max_height` and `max_height`
        """
