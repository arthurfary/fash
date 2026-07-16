"""Semantic representation of a single keypress.

A `Key` is either a `SpecialKey` (an arrow, Enter, Escape, ...) or a plain
`str` holding the single character that was typed. Widgets pattern-match on
this union to decide what a keypress means to them, instead of dealing with
raw bytes / escape sequences themselves.
"""

from enum import Enum, auto

ESC = "\x1b"


class SpecialKey(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    BACKSPACE = auto()
    TAB = auto()
    ESCAPE = auto()
    CTRL_C = auto()


Key = SpecialKey | str
"""A decoded keypress: a `SpecialKey`, or a single printable character."""

# Keys that arrive as a single, unambiguous byte.
SIMPLE_KEYS: dict[str, SpecialKey] = {
    "\r": SpecialKey.ENTER,
    "\n": SpecialKey.ENTER,
    "\x7f": SpecialKey.BACKSPACE,
    "\t": SpecialKey.TAB,
    "\x03": SpecialKey.CTRL_C,
}

# Final byte of an `ESC [ <byte>` CSI sequence, as sent by the arrow keys.
ARROW_KEYS: dict[str, SpecialKey] = {
    "A": SpecialKey.UP,
    "B": SpecialKey.DOWN,
    "C": SpecialKey.RIGHT,
    "D": SpecialKey.LEFT,
}
