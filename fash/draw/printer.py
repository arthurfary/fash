from fash.core.cell import Color, Style
from .styles import ANSI_COLOR_MAP, ANSI_RESET, BOLD

class Printer:
    def __init__(self):
        self._needs_reset = False
    
    def print(self, row: int, col: int, char: str = "", style: Style = Style()):
        self._needs_reset = False
        print(
            self._cursor_to(row, col)
            + self._color(style.color)
            + self._bold(style.bold)
            + char
            + self._reset()
            , end=""
        )
    
    def _cursor_to(self, row: int, col: int) -> str:
        """ANSI escape to move cursor; row/col are 0-indexed."""
        return f"\033[{row + 1};{col + 1}H"
    
    def _color(self, color: Color | None) -> str:
        if (color is not None):
            self._needs_reset = True
            return ANSI_COLOR_MAP[color]
        return ""
    
    def _bold(self, bold: bool) -> str:
        if (bold):
            self._needs_reset = True
            return BOLD[True]
        return ""
    
    def _reset(self) -> str:
        return ANSI_RESET if self._needs_reset else ""
    
    def clear_screen(self):
        print("\033[2J", end="")
    
    def next_line(self):
        print("\n", end="")


    

