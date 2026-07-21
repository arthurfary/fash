from contextlib import contextmanager
from fash.core.exceptions import CursorPositionError
from typing import Tuple
from io import UnsupportedOperation
from typing import Iterator
import os
import re
import select
import sys
import termios
import tty

from fash.core.keys import ARROW_KEYS, ESC, SIMPLE_KEYS, Key, SpecialKey


class Reader:
    def __init__(self):
        """Get file descriptor from terminal where this python code is running"""
        try:
            self.file_descriptor: int = sys.stdin.fileno()
        except UnsupportedOperation:
            """
            TODO: Refactor and define a terminal reading strategy
                - This exception only happens in pytest. Reader should extend a BaseReader class and pytest 
                must create a FakeReader passed to drawer through Dependency Injection
                - We need to determine if a Reader class really should be in the draw module
                - Currently there is no definition on how user input will be defined and handled in widgets
                so this class is a 'temporary' measure wich only solves the drawer need for the current cursor position
            """
            pass

    def save_terminal_settings(self):
        self.terminal_settings = termios.tcgetattr(self.file_descriptor)

    def restore_last_terminal_settings(self):
        termios.tcsetattr(self.file_descriptor, termios.TCSADRAIN, self.terminal_settings)

    def enter_raw_mode(self):
        tty.setraw(self.file_descriptor)

    @contextmanager
    def raw_mode(self) -> Iterator["Reader"]:
        """Put the terminal into raw mode for the duration of the block.

        Terminal settings are always restored on exit, even if the block
        raises - the context manager equivalent of the try/finally dance
        `termios` requires:

            with reader.raw_mode():
                for key in reader.keys():
                    ...
        """
        self.save_terminal_settings()
        self.enter_raw_mode()
        try:
            yield self
        finally:
            self.restore_last_terminal_settings()

    def read_key(self, escape_timeout: float = 0.01) -> Key:
        """Block until a key is pressed and return it as a decoded `Key`.

        Must be called from inside a `raw_mode()` block. Bytes are read
        straight off the raw file descriptor via `os.read` - never through
        `sys.stdin`'s buffer - so the `select` check below can reliably
        tell an ESC keypress apart from the start of an arrow-key escape
        sequence (mixing buffered reads with `select` on the same fd is a
        classic source of "arrow keys randomly don't work" bugs).
        """
        char = self._read_byte()

        if char in SIMPLE_KEYS:
            return SIMPLE_KEYS[char]

        if char != ESC:
            return char

        # A lone Escape keypress has nothing following it; an arrow key
        # (and friends) sends `ESC [ <byte>` as one uninterrupted burst.
        # `select` with a short timeout tells them apart without blocking
        # on a keypress that may never come.
        if not select.select([self.file_descriptor], [], [], escape_timeout)[0]:
            return SpecialKey.ESCAPE

        if self._read_byte() != "[":
            return SpecialKey.ESCAPE

        return ARROW_KEYS.get(self._read_byte(), SpecialKey.ESCAPE)

    def keys(self) -> Iterator[Key]:
        """Yield decoded keypresses until the input stream closes.

        Meant to be driven from inside a `raw_mode()` block:

            with reader.raw_mode():
                for key in reader.keys():
                    if key is SpecialKey.CTRL_C:
                        break
                    ...
        """
        while True:
            try:
                yield self.read_key()
            except EOFError:
                return

    def _read_byte(self) -> str:
        data = os.read(self.file_descriptor, 1)
        if not data:
            raise EOFError
        return data.decode(errors="ignore")

    def get_cursor_pos(self) -> Tuple[int, int]:
        self.save_terminal_settings()
        self.enter_raw_mode()

        print("\033[6n", end="")
        sys.stdout.flush()

        response = ""

        while True:
            ch = sys.stdin.read(1)
            response += ch
            if ch == "R":
                break

        self.restore_last_terminal_settings()

        match = re.search(r"\[(\d+);(\d+)R", response)

        if not match:
            raise CursorPositionError("Reader: Could not read cursor position")

        row, col = int(match.group(1)), int(match.group(2))

        return row, col
