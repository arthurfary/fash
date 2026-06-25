from fash.core.cell import Cell


# TODO:write a "set" and a "write" method:
# - Set: sets char at pos (check inside grid)
# - Write: writes a string in char form (for char in string, write to cell starting at row,col)
class CellGrid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

        self.cells: list[list[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def set(self, row: int, col: int, character: str, **style):
        if len(character) != 1:
            raise ValueError("CellGrid: set character must be of length 1")

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col] = Cell(character, **style)

    def write(self, row_start: int, col: int, text: str, **style):
        for i, char in enumerate(text):
            if 0 <= row_start < self.rows and 0 <= col < self.cols:
                self.cells[row_start][col + i] = Cell(char, **style)

    def __str__(self) -> str:
        return str([col for col in [row for row in self.cells]])
