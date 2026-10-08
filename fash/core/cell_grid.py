from fash.core.cell import Cell, Style
from fash.core.exceptions import InvalidCharacterLengthError


class CellGrid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

        self.cells: list[list[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def set(self, row: int, col: int, character: str, style: Style):
        if len(character) != 1:
            raise InvalidCharacterLengthError("CellGrid: Set character must be of length 1")

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col] = Cell(character, style)

    def write(self, row_start: int, col: int, text: str, style: Style):
        for i, char in enumerate(text):
            if 0 <= row_start < self.rows and 0 <= col < self.cols:
                self.cells[row_start][col + i] = Cell(char, style)

    def __str__(self) -> str:
        return str(self.cells)
