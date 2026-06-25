from fash.core.cell_grid import CellGrid
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window


class Drawer:
    def __init__(self, lines: int, columns: int, root_window: Window, window_separator: str = "") -> None:
        num_rows = len(root_window.grid)
        num_cols = len(root_window.grid[0])

        self.total_lines = lines
        self.total_columns = columns
        self.window_separator = window_separator
        self.root_window = root_window

        self.row_heights = self._distribute_sizes(lines, num_rows)
        self.col_widths = self._distribute_sizes(columns, num_cols)

    @staticmethod
    def _distribute_sizes(total: int, count: int) -> list[int]:
        """Distributes `total` units across `count` slots as evenly as possible.
        Slots at the beginning receive an extra unit when total is not evenly divisible.
        """
        base, remainder = divmod(total, count)
        return [base + 1] * remainder + [base] * (count - remainder)

    def draw_all(self):
        # TODO: When decided what to do when grid pos is none
        for row_count, (row, row_height) in enumerate(zip(self.root_window.grid, self.row_heights)):
            for col_count, (window, col_width) in enumerate(zip(row, self.col_widths)):
                if not window:
                    continue

                grid = window.draw(row_height, col_width)

                self._draw_widget(row_count, col_count, grid)

    def _draw_widget(self, window_row: int, window_col: int, grid: CellGrid):
        for row_count, row in enumerate(grid.cells):
            for col_count, cell in enumerate(row):
                # TODO: ABSTRACT THIS PRINTING LOGIC
                print(
                    f"\033[{sum(self.row_heights[0:window_row]) + row_count + 1};{sum(self.col_widths[0:window_col]) + col_count + 1}H"
                    # f"\033[{window_row * self.max_lines_per_window + row_count + 1};{window_col * self.max_columns_per_window + col_count + 1}H"
                    + cell.char
                )


