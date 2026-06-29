from fash.core.cell import Color, Style
from fash.draw.ansi import AnsiCodes, AnsiFormatter


class Printer:
    def print(self, row: int, col: int, char: str = "", style: Style = Style()):
        needs_reset = style.color is not None or style.bold  # decided upfront, not via side effects
        print(
            AnsiFormatter.move_cursor(row, col)
            + self._color(style.color)
            + self._bold(style.bold)
            + char
            + (AnsiCodes.RESET if needs_reset else ""),
            end="",
        )

    def _color(self, color: Color | None) -> str:
        return AnsiCodes.COLOR_MAP[color] if color is not None else ""

    def _bold(self, bold: bool) -> str:
        return AnsiCodes.BOLD if bold else ""

    def clear_screen(self):
        print(AnsiCodes.CLEAR_SCREEN, end="")

    def next_line(self):
        print("\n", end="")

