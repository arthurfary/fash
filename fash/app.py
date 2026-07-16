from __future__ import annotations

from typing import Iterable

from fash.core.signal import Signal
from fash.core.widget import Widget
from fash.draw.drawer import Drawer
from fash.draw.keys import Key, SpecialKey


class App:
    DEFAULT_QUIT_KEYS: frozenset[Key] = frozenset({SpecialKey.CTRL_C})

    def __init__(
        self,
        drawer: Drawer,
        focused_widget: Widget | None = None,
        quit_keys: Iterable[Key] = DEFAULT_QUIT_KEYS,
    ) -> None:
        self.drawer = drawer
        self.reader = drawer.reader  # share the Drawer's Reader - one raw-mode owner
        self.focused_widget = focused_widget
        self.quit_keys = frozenset(quit_keys)

    def draw(self) -> None:
        """Render a snapshot of the current state."""
        self.drawer.draw_all()

    def run(self) -> None:
        """Draw, then block - reading keys, dispatching to the focused
        widget, and redrawing and/or quitting based on what it reports -
        until a quit key is pressed.

        `quit_keys` (Ctrl-C by default) is a global escape hatch that
        works no matter what's focused. `Signal.QUIT` from the focused
        widget's `handle_key` is the widget's *own* choice to end things -
        e.g. a `ListWidget` whose selection callback decides a pick is
        final. Both are honored; neither replaces the other.
        """
        self.draw()

        with self.reader.raw_mode():
            for key in self.reader.keys():
                if key in self.quit_keys:
                    return

                if self.focused_widget is None:
                    continue

                signal = self.focused_widget.handle_key(key)
                if Signal.REDRAW in signal:
                    self.draw()
                if Signal.QUIT in signal:
                    return
