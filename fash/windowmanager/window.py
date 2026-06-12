from fash.widgets.base_widget import Widget


class Window:
    pass

    def __init__(self, row: int, col: int):
        self.grid: list[list[Widget | None]] = [[None for _ in range(col)] for _ in range(row)]
        # self.make_grid(row, col) --> call only of need resizing

    def make_grid(self, row: int, col: int):
        row_list = []
        for _ in range(row):
            col_list = []
            for _ in range(col):
                col_list.append(None)  # TODO: base widget class? specific widget for blank window in grid?
            row_list.append(col_list)

        self.grid = row_list

    def get_at(self, row: int, col: int) -> Widget | None:
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise IndexError

        return self.grid[row][col]

    def set_at(self, row: int, col: int, widget: Widget):
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise IndexError

        self.grid[row][col] = widget
