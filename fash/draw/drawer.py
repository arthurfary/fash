from fash.core.cell_grid import CellGrid
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window


class Drawer:
    def __init__(self, lines: int, columns: int, root_window: Window, window_separator: str = "") -> None:

        num_rows, num_cols = root_window.get_grid_size()

        self.total_lines = lines
        self.total_columns = columns
        self.root_window = root_window
        self.row_heights = self._distribute_sizes(lines, num_rows)
        self.col_widths = self._distribute_sizes(columns, num_cols)

        if len(window_separator) not in [0, 1]:
            raise ValueError("Window separator must be 0 or 1 character.")
        self.window_separator = window_separator

    def draw_all(self):
        num_rows = len(self.root_window.grid)

        for row_idx, (row, row_height) in enumerate(zip(self.root_window.grid, self.row_heights)):
            is_last_row = row_idx == num_rows - 1
            start_row = sum(self.row_heights[:row_idx])

            for col_idx, (window, col_width) in enumerate(zip(row, self.col_widths)):
                if not window:
                    continue

                is_last_col = col_idx == len(row) - 1
                start_col = sum(self.col_widths[:col_idx])

                content_height = row_height - (1 if self.window_separator and not is_last_row else 0)
                content_width = col_width - (1 if self.window_separator and not is_last_col else 0)

                grid = window.draw(content_height, content_width)
                self._draw_content(grid, start_row, start_col)

                if self.window_separator:
                    self._draw_separators(grid, start_row, start_col, is_last_row, is_last_col)

    def _draw_content(self, grid: CellGrid, start_row: int, start_col: int):
        for row_idx, row in enumerate(grid.cells):
            for col_idx, cell in enumerate(row):
                print(self._cursor_to(start_row + row_idx, start_col + col_idx) + cell.char)

    def _draw_separators(self, grid: CellGrid, start_row: int, start_col: int, is_last_row: bool, is_last_col: bool):
        height = len(grid.cells)
        width = len(grid.cells[0]) if grid.cells else 0

        if not is_last_col:
            for row_idx in range(height):
                print(self._cursor_to(start_row + row_idx, start_col + width) + self.window_separator)

        if not is_last_row:
            for col_idx in range(width):
                print(self._cursor_to(start_row + height, start_col + col_idx) + self.window_separator)

            if not is_last_col:
                print(self._cursor_to(start_row + height, start_col + width) + self.window_separator)

    @staticmethod
    def _distribute_sizes(total: int, count: int) -> list[int]:
        base, remainder = divmod(total, count)
        return [base + 1] * remainder + [base] * (count - remainder)

    def _cursor_to(self, row: int, col: int) -> str:
        """ANSI escape to move cursor; row/col are 0-indexed."""
        return f"\033[{row + 1};{col + 1}H"
