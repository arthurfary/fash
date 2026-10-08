from typing import Callable, Unpack

from fash.core.cell import Color, Style
from fash.core.cell_grid import CellGrid
from fash.core.keys import Key, SpecialKey
from fash.core.signal import Signal
from fash.core.widget import Widget
from fash.widgets.style import WidgetStyle


class ListWidget(Widget):
    def __init__(
        self,
        title: str,
        description: str,
        items: list[str],
        callback: Callable[[str], Signal | None],
        **style: Unpack[WidgetStyle],
    ) -> None:
        self.title = title
        self.description = description
        self.items = items
        self.index = 0
        self.callback = callback
        self.main_color: Color | None = style.get("color")

    @property
    def selected_item(self) -> str:
        """The selected value"""
        return self.items[self.index]

    def draw(self, max_rows: int, max_cols: int) -> CellGrid:
        out = [self.title.center(max_cols, " ")]
        out.append(self.description)

        for i, item in enumerate(self.items):
            out.append("> " + item if i == self.index else item)

        grid = CellGrid(max_rows, max_cols)
        for i, line in enumerate(out):
            grid.write(row_start=i, col=0, text=line, style=Style(color=self.main_color))

        return grid

    def handle_key(self, key: Key) -> Signal:
        match key:
            case SpecialKey.UP if self.index > 0:
                self.index -= 1
                return Signal.REDRAW
            case SpecialKey.DOWN if self.index < len(self.items) - 1:
                self.index += 1
                return Signal.REDRAW
            case SpecialKey.ENTER:
                return self.callback(self.items[self.index]) or Signal.NONE
            case _:
                return Signal.NONE
