from enum import Flag, auto


class Signal(Flag):
    NONE = 0
    REDRAW = auto()
    QUIT = auto()
