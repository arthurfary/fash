from fash.core.cell_grid import CellGrid
from fash.widgets.base_widget import Widget
import textwrap
from fash.core.cell import Cell


class TextWidget(Widget):
    def __init__(self, title: str, text: str) -> None:
        self.title = title
        self.text = text
        self.PADDING_CHAR = "."

    def draw(self, max_width, max_height) -> CellGrid:
        out_str = self.title.center(max_width, self.PADDING_CHAR) + "\n"
        out_str = textwrap.fill(
            out_str + self.text,
            max_width,
            max_lines=max_height,
        )

        grid = CellGrid(max_width, max_height)
        for i, line in enumerate(out_str.splitlines()):
            grid.write(i, 0, line)

        return grid
