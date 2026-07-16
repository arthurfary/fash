from fash.core.cell import Color, Style
import os
from typing import Literal, Tuple
from fash.draw.reader import Reader
from fash.draw.printer import Printer
from fash.core.cell_grid import CellGrid
from fash.windowmanager.window import Window


class Drawer:
    def __init__(
        self,
        lines: int,
        columns: int,
        root_window: Window,
        window_separator: str = "",
        separator_color: Color = Color.DEFAULT,
        render_mode: Literal["absolute", "dynamic"] = "absolute",
        printer: Printer | None = None,
        reader: Reader | None = None,
    ) -> None:

        num_rows, num_cols = root_window.get_grid_size()

        self.total_lines = lines
        self.total_columns = columns
        self.root_window = root_window
        self.row_heights = self._distribute_sizes(lines, num_rows)
        self.col_widths = self._distribute_sizes(columns, num_cols)

        self.rows_start_pos = self._calculate_start_positions(self.row_heights)
        self.cols_start_pos = self._calculate_start_positions(self.col_widths)

        self.printer = printer or Printer()
        self.reader = reader or Reader()

        self.render_mode: Literal["absolute", "dynamic"] = render_mode
        self.row_offset = 0

        self.calculate_row_offset()

        if len(window_separator) not in [0, 1]:
            raise ValueError("Window separator must be 0 or 1 character.")
        self.window_separator = window_separator
        self.separator_color = separator_color

    @staticmethod
    def _calculate_start_positions(sizes: list[int]) -> list[int]:
        """Returns the start positions based on the available heights/widths"""
        starts = [0]
        for size in sizes:
            starts.append(starts[-1] + size)
        return starts

    def calculate_row_offset(self):
        if self.render_mode == "dynamic":
            cursor_row, _ = self.reader.get_cursor_pos()
            terminal_rows, _ = self._get_terminal_size()

            space_needed = self.total_lines
            space_available = terminal_rows - cursor_row

            if space_available < space_needed:
                lines_to_scroll = space_needed - space_available
                print("\n" * lines_to_scroll, end="")
                self.row_offset = terminal_rows - space_needed + 1
            else:
                self.row_offset = cursor_row

    def draw_all(self):
        if self.render_mode == "absolute":
            self.printer.clear_screen()

        num_rows = len(self.root_window.grid)

        for row_idx, (row, row_height) in enumerate(zip(self.root_window.grid, self.row_heights)):
            is_last_row = row_idx == num_rows - 1

            for col_idx, (window, col_width) in enumerate(zip(row, self.col_widths)):
                if not window:
                    continue

                is_last_col = col_idx == len(row) - 1

                content_height = row_height - (1 if self.window_separator and not is_last_row else 0)
                content_width = col_width - (1 if self.window_separator and not is_last_col else 0)

                grid = window.draw(content_height, content_width)
                self._draw_content(grid, self.rows_start_pos[row_idx], self.cols_start_pos[col_idx])

                if self.window_separator:
                    self._draw_separators(
                        grid, self.rows_start_pos[row_idx], self.cols_start_pos[col_idx], is_last_row, is_last_col
                    )

        self.printer.next_line()

    def _draw_content(self, grid: CellGrid, start_row: int, start_col: int):
        for row_idx, row in enumerate(grid.cells):
            for col_idx, cell in enumerate(row):
                self.printer.print(start_row + row_idx + self.row_offset, start_col + col_idx, cell.char, cell.style)

    def _draw_separators(self, grid: CellGrid, start_row: int, start_col: int, is_last_row: bool, is_last_col: bool):
        height = len(grid.cells)
        width = len(grid.cells[0]) if grid.cells else 0

        if not is_last_col:
            for row_idx in range(height):
                self.printer.print(
                    start_row + row_idx + self.row_offset,
                    start_col + width,
                    self.window_separator,
                    Style(color=self.separator_color),
                )

        if not is_last_row:
            for col_idx in range(width):
                self.printer.print(
                    start_row + height + self.row_offset,
                    start_col + col_idx,
                    self.window_separator,
                    Style(color=self.separator_color),
                )

            if not is_last_col:
                self.printer.print(
                    start_row + height + self.row_offset,
                    start_col + width,
                    self.window_separator,
                    Style(color=self.separator_color),
                )

    @staticmethod
    def _distribute_sizes(total: int, count: int) -> list[int]:
        base, remainder = divmod(total, count)
        return [base + 1] * remainder + [base] * (count - remainder)

    @staticmethod
    def _get_terminal_size() -> Tuple[int, int]:
        col, row = os.get_terminal_size()
        return row, col
