from fash.windowmanager.window import Window


class Drawer:
    def __init__(self, lines: int, columns: int, root_window: Window) -> None:
        self.total_lines = lines
        self.total_columns = columns

        # TODO: Floor division may divide too much, calculate all spaces before?
        self.max_lines_per_window = lines // root_window.row_count
        self.max_columns_per_window = columns // root_window.col_count

        self.root_window = root_window

    def draw_all(self):
        # TODO: When decided what to do when grid pos is none

        print_str = (("." * self.total_columns) + "\n") * self.total_lines

        for pos_row, row in enumerate(self.root_window.grid):
            for pos_col, col in enumerate(row):
                try:
                    col.draw()
                except:
                    print(col)
