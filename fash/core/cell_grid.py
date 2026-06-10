from fash.core.cell import Cell, Style


# TODO:write a "set" and a "write" method:
# - Set: sets char at pos (check inside grid)
# - Write: writes a string in char form (for char in string, write to cell starting at row,col)
class CellGrid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

        self.cells: list[list[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
