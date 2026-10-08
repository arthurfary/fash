from fash.core.exceptions import WidgetOutOfBoundsError
from fash.core.widget import Widget


class Window:
    def __init__(self, row: int, col: int):
        self.grid: list[list[Widget | None]] = [[None for _ in range(col)] for _ in range(row)]

    def get_grid_size(self) -> tuple[int, int]:
        if len(self.grid) == 0:
            return 0, 0
        return len(self.grid), len(self.grid[0])

    def get_at(self, row: int, col: int) -> Widget | None:
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise WidgetOutOfBoundsError(f"row: {row} col: {col} not inbound.")

        return self.grid[row][col]

    def set_at(self, row: int, col: int, widget: Widget):
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise WidgetOutOfBoundsError(f"row: {row} col: {col} not inbound.")

        self.grid[row][col] = widget

    def __str__(self) -> str:
        return str(self.grid)
