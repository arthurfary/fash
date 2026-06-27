from fash.core.cell import Color

ANSI_COLOR_MAP: dict[Color, str] = {
    Color.DEFAULT: "\033[39m",
    Color.RED: "\033[31m",
    Color.GREEN: "\033[32m",
    Color.BLUE: "\033[34m",
    Color.YELLOW: "\033[33m",
}

ANSI_RESET = "\033[0m"

BOLD = {
    True: "\033[1m",
    False: "\x1b[22m" #disables bold only
}