from fash.core.cell import Color


class AnsiCodes:
    """ANSI escape sequence constants."""

    CURSOR_HOME = "\033[H"
    CLEAR_SCREEN = "\033[2J"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    # BOLD = {True: "\033[1m", False: "\x1b[22m"}

    COLOR_DEFAULT = "\033[39m"
    COLOR_RED = "\033[31m"
    COLOR_GREEN = "\033[32m"
    COLOR_BLUE = "\033[34m"
    COLOR_YELLOW = "\033[33m"
    COLOR_MAP = {
        Color.DEFAULT: COLOR_DEFAULT,
        Color.RED: COLOR_RED,
        Color.GREEN: COLOR_GREEN,
        Color.BLUE: COLOR_BLUE,
        Color.YELLOW: COLOR_YELLOW,
    }


class AnsiFormatter:
    """Format ANSI escape sequences."""

    @staticmethod
    def move_cursor(row: int, col: int) -> str:
        """Position cursor at (row, col), 0-indexed."""
        return f"\033[{row + 1};{col + 1}H"

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove all ANSI escape sequences from text."""
        import re

        return re.sub(r"\x1b\[[^A-Za-z]*[A-Za-z]", "", text)
