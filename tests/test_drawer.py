from fash.draw.drawer import Drawer
import pytest
import re
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[^A-Za-z]*[A-Za-z]", "", text)


@pytest.fixture
def full_window():
    w = Window(2, 2)
    widget = TextWidget("Title", "Body text")
    for row in range(2):
        for col in range(2):
            w.set_at(row, col, widget)
    return w


@pytest.fixture
def sparse_window():
    w = Window(2, 2)
    w.set_at(0, 0, TextWidget("Title", "Body text"))
    return w  # remaining 3 cells are None


def parse_terminal_grid(raw: str, rows: int, cols: int) -> list[list[str]]:
    """Reconstruct a 2D grid from ANSI cursor-positioning output."""
    grid = [[" "] * cols for _ in range(rows)]
    for match in re.finditer(r"\x1b\[(\d+);(\d+)H(.)", raw):
        row = int(match.group(1)) - 1  # ANSI is 1-indexed
        col = int(match.group(2)) - 1
        char = match.group(3)
        if 0 <= row < rows and 0 <= col < cols:
            grid[row][col] = char
    return grid


# --- _distribute_sizes ---


def test_distribute_sizes_even_split():
    assert Drawer._distribute_sizes(10, 2) == [5, 5]


def test_distribute_sizes_remainder_goes_to_front():
    assert Drawer._distribute_sizes(10, 3) == [4, 3, 3]


def test_distribute_sizes_sum_equals_total():
    assert sum(Drawer._distribute_sizes(17, 5)) == 17


def test_distribute_sizes_slot_count():
    assert len(Drawer._distribute_sizes(17, 5)) == 5


# --- Drawer constructor ---


def test_row_heights_sum_equals_lines(full_window):
    d = Drawer(25, 100, full_window)
    assert sum(d.row_heights) == 25


def test_col_widths_sum_equals_columns(full_window):
    d = Drawer(25, 100, full_window)
    assert sum(d.col_widths) == 100


# --- draw_all ---


def test_draw_all_produces_output(full_window, capsys):
    Drawer(25, 100, full_window).draw_all()
    assert len(capsys.readouterr().out) > 0


def test_draw_all_output_contains_ansi_codes(full_window, capsys):
    Drawer(25, 100, full_window).draw_all()
    assert "\033[" in capsys.readouterr().out


def test_draw_all_skips_none_cells(capsys):
    w = Window(2, 2)  # all cells are None
    Drawer(25, 100, w).draw_all()
    assert capsys.readouterr().out == ""


def test_draw_all_renders_widget_content(sparse_window, capsys):
    Drawer(25, 100, sparse_window).draw_all()
    clean = strip_ansi(capsys.readouterr().out).replace("\n", "")
    assert "Title" in clean


def test_separator_vertical_column(full_window, capsys):
    rows, cols = 25, 100
    Drawer(rows, cols, full_window, "#").draw_all()
    grid = parse_terminal_grid(capsys.readouterr().out, rows, cols)

    # separator sits at the boundary of the first window's column allocation
    sep_col = Drawer._distribute_sizes(cols, 2)[0] - 1  # 49, 0-indexed
    assert all(grid[row][sep_col] == "#" for row in range(rows))


def test_separator_horizontal_row(full_window, capsys):
    rows, cols = 25, 100
    Drawer(rows, cols, full_window, "#").draw_all()
    grid = parse_terminal_grid(capsys.readouterr().out, rows, cols)

    sep_row = Drawer._distribute_sizes(rows, 2)[0] - 1  # 12, 0-indexed
    assert all(grid[sep_row][col] == "#" for col in range(cols))
