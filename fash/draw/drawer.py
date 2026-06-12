from fash.core.cell_grid import CellGrid
from fash.widgets.base_widget import Widget
from fash.windowmanager.window import Window


class Drawer:
    def __init__(self, lines: int, columns: int, root_window: Window) -> None:
        self.total_lines = lines
        self.total_columns = columns

        # TODO: Floor division may divide too much, calculate all spaces before?
        self.max_lines_per_window = lines // len(root_window.grid)
        self.max_columns_per_window = columns // len(root_window.grid[0])  # should have clearer variable names

        self.root_window = root_window

    def draw_all(self):
        # TODO: When decided what to do when grid pos is none
        for row_count, row in enumerate(self.root_window.grid):
            for col_count, window in enumerate(row):
                if not window:
                    continue

                widget = window.draw(
                    self.max_lines_per_window * (row_count + 1), self.max_columns_per_window * (col_count + 1)
                )

                self._draw_widget(row_count, col_count, widget)

    def _draw_widget(self, window_row: int, window_col: int, grid: CellGrid):
        for row_count, row in enumerate(grid.cells):
            for col_count, cell in enumerate(row):
                print(
                    f"\033[{window_row * self.max_lines_per_window + row_count};{window_col * self.max_columns_per_window + col_count}H"
                    + cell.char
                )
