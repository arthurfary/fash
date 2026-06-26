from fash.core.cell import Style
from fash.core.cell_grid import CellGrid
from fash.widgets.base_widget import Widget
import textwrap


class TextWidget(Widget):
    def __init__(self, title: str, text: str, style: Style = Style()) -> None:
        self.title = title
        self.text = text
        self.PADDING_CHAR = "."
        self.style: Style = style

    def draw(self, max_rows: int, max_cols: int) -> CellGrid:
        out_str = self.title.center(max_cols, self.PADDING_CHAR) + "\n"
        out_str = textwrap.fill(
            out_str + self.text,
            max_cols,
            max_lines=max_rows,
        )

        grid = CellGrid(max_rows, max_cols)
        for i, line in enumerate(out_str.splitlines()):
            grid.write(row_start=i, col=0, text=line, style=self.style)

        return grid

    def __str__(self) -> str:
        return str(self.draw(10, 10))
