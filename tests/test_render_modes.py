import pytest
import re
from fash.draw.drawer import Drawer
from fash.draw.reader import Reader
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window
import os
import unittest.mock as mock


# ── Fakes ──────────────────────────────────────────────────────────────────────

class FakeReader(Reader):
    def __init__(self, cursor_row: int = 1, cursor_col: int = 1, terminal_rows: int = 30):
        self._cursor_row = cursor_row
        self._cursor_col = cursor_col

    def get_cursor_pos(self) -> tuple[int, int]:
        return self._cursor_row, self._cursor_col


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def simple_window():
    w = Window(1, 1)
    w.set_at(0, 0, TextWidget("Title", "Body"))
    return w


def make_drawer(window, lines=10, columns=100, cursor_row=1, cursor_col=1, terminal_rows=30):
    reader = FakeReader(cursor_row=cursor_row, cursor_col=cursor_col)
    fake_terminal_size = os.terminal_size((columns, terminal_rows))  # (columns, lines)
    with mock.patch("os.get_terminal_size", return_value=fake_terminal_size):
        return Drawer(lines, columns, window, render_mode="dynamic", reader=reader)


# ── Testes: row_offset sem scroll ──────────────────────────────────────────────

class TestDynamicNoScroll:
    def test_row_offset_equals_cursor_row_when_space_available(self, simple_window):
        d = make_drawer(simple_window, lines=10, cursor_row=5, terminal_rows=30)
        assert d.row_offset == 5

    def test_row_offset_at_top_of_terminal(self, simple_window):
        d = make_drawer(simple_window, lines=10, cursor_row=1, terminal_rows=30)
        assert d.row_offset == 1

    def test_content_positioned_at_cursor_row(self, simple_window, capsys):
        d = make_drawer(simple_window, lines=10, cursor_row=5, terminal_rows=30)
        d.draw_all()
        out = capsys.readouterr().out
        first_position = re.search(r"\x1b\[(\d+);(\d+)H", out)
        assert first_position is not None
        assert int(first_position.group(1)) == 6  # 1-indexed: row_offset=5, start_row=0 → linha 6


# ── Testes: scroll ─────────────────────────────────────────────────────────────

class TestDynamicScroll:
    def test_scroll_happens_when_no_space(self, simple_window, capsys):
        make_drawer(simple_window, lines=10, cursor_row=28, terminal_rows=30)
        out = capsys.readouterr().out
        assert "\n" in out

    def test_scroll_amount_is_correct(self, simple_window, capsys):
        # cursor_row=28, terminal_rows=30, total_lines=10
        # space_available = 30 - 28 = 2, lines_to_scroll = 10 - 2 = 8
        make_drawer(simple_window, lines=10, cursor_row=28, terminal_rows=30)
        out = capsys.readouterr().out
        assert out.count("\n") == 8

    def test_row_offset_after_scroll(self, simple_window):
        # terminal_rows=30, total_lines=10 → row_offset = 30 - 10 + 1 = 21
        d = make_drawer(simple_window, lines=10, cursor_row=28, terminal_rows=30)
        assert d.row_offset == 21

    def test_row_offset_cursor_at_last_line(self, simple_window):
        # cursor_row=30, terminal_rows=30, total_lines=10 → row_offset = 21
        d = make_drawer(simple_window, lines=10, cursor_row=30, terminal_rows=30)
        assert d.row_offset == 21

    def test_no_scroll_when_exactly_enough_space(self, simple_window, capsys):
        # cursor_row=20, terminal_rows=30, total_lines=10 → space_available=10, sem scroll
        make_drawer(simple_window, lines=10, cursor_row=20, terminal_rows=30)
        out = capsys.readouterr().out
        assert "\n" not in out

    def test_content_starts_at_correct_row_after_scroll(self, simple_window, capsys):
        d = make_drawer(simple_window, lines=10, cursor_row=28, terminal_rows=30)
        capsys.readouterr()  # descarta o scroll
        d.draw_all()
        out = capsys.readouterr().out
        first_position = re.search(r"\x1b\[(\d+);(\d+)H", out)
        assert first_position is not None
        assert int(first_position.group(1)) == 22  # row_offset=21, start_row=0 → linha 22