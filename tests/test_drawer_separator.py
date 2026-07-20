from fash.core.cell import Color, Style
from fash.core.cell_grid import CellGrid
from fash.core.widget import Widget
from fash.draw.drawer import Drawer
from fash.windowmanager.window import Window
import pytest
from unittest.mock import MagicMock
from fash.draw.printer import Printer
from fash.draw.reader import Reader
from fash.widgets.text_widget import TextWidget


class DummyWidget(Widget):
    def draw(self, max_rows: int, max_cols: int) -> CellGrid:
        grid = CellGrid(max_rows, max_cols)
        grid.set(0, 0, "X", Style())
        return grid


def _make_two_column_window() -> Window:
    root_window = Window(1, 2)
    root_window.set_at(0, 0, DummyWidget())
    root_window.set_at(0, 1, DummyWidget())
    return root_window


def test_draw_all_renders_window_separator_between_windows(capsys):
    drawer = Drawer(2, 8, _make_two_column_window(), window_separator="|")

    drawer.draw_all()

    output = capsys.readouterr().out
    assert "|" in output


def test_draw_all_applies_separator_color(capsys):
    drawer = Drawer(
        2,
        8,
        _make_two_column_window(),
        window_separator="|",
        separator_color=Color.RED,
    )

    drawer.draw_all()

    output = capsys.readouterr().out
    assert "|" in output
    assert "\033[31m" in output
    assert "\033[0m" in output

def make_reader(cursor_pos=(1, 1)):
    reader = MagicMock(spec=Reader)
    reader.get_cursor_pos.return_value = cursor_pos
    return reader


def make_printer():
    return MagicMock(spec=Printer)


def make_drawer(
    lines=20,
    columns=40,
    window=None,
    separator="|",
    separator_color=Color.DEFAULT,
    printer=None,
    reader=None,
):
    if window is None:
        window = Window(1, 1)
        window.set_at(0, 0, TextWidget("T", "B"))
    return Drawer(
        lines=lines,
        columns=columns,
        root_window=window,
        window_separator=separator,
        separator_color=separator_color,
        printer=printer or make_printer(),
        reader=reader or make_reader(),
    )


# ---------------------------------------------------------------------------
# Constructor validation
# ---------------------------------------------------------------------------


def test_separator_empty_string_is_valid():
    """Empty separator is allowed."""
    d = make_drawer(separator="")
    assert d.window_separator == ""


def test_separator_single_char_is_valid():
    """Single-character separator is allowed."""
    d = make_drawer(separator="|")
    assert d.window_separator == "|"


def test_separator_two_chars_raises():
    """Separator with 2+ characters must raise ValueError."""
    with pytest.raises(ValueError):
        make_drawer(separator="||")


def test_separator_long_string_raises():
    """Long string must raise ValueError."""
    with pytest.raises(ValueError):
        make_drawer(separator="---")


# ---------------------------------------------------------------------------
# Vertical separator (between columns)
# ---------------------------------------------------------------------------


def test_vertical_separator_drawn_between_columns():
    """The separator character must appear in the column right after the content."""
    w = Window(1, 2)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(0, 1, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    printed_chars = [c[0][2] for c in printer.print.call_args_list]
    assert "|" in printed_chars


def test_vertical_separator_not_drawn_after_last_column():
    """The separator must NOT be drawn after the last column."""
    w = Window(1, 2)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(0, 1, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    col_widths = d.col_widths
    last_col_start = d.cols_start_pos[1]
    last_col_end = last_col_start + col_widths[1]

    separator_cols = [
        c[0][1]  # col arg of printer.print
        for c in printer.print.call_args_list
        if c[0][2] == "|"
    ]
    assert all(col < last_col_end for col in separator_cols), (
        "Separator was drawn beyond the last column"
    )


def test_single_column_no_vertical_separator():
    """With only 1 column, no vertical separator must be drawn."""
    w = Window(1, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c for c in printer.print.call_args_list if c[0][2] == "|"]
    assert separator_calls == []


# ---------------------------------------------------------------------------
# Horizontal separator (between rows)
# ---------------------------------------------------------------------------


def test_horizontal_separator_drawn_between_rows():
    """The separator character must appear in the row right after the content."""
    w = Window(2, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(1, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="-", printer=printer, reader=make_reader())
    d.draw_all()

    printed_chars = [c[0][2] for c in printer.print.call_args_list]
    assert "-" in printed_chars


def test_horizontal_separator_not_drawn_after_last_row():
    """The separator must NOT be drawn after the last row."""
    w = Window(2, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(1, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="-", printer=printer, reader=make_reader())
    d.draw_all()

    row_heights = d.row_heights
    last_row_start = d.rows_start_pos[1]
    last_row_end = last_row_start + row_heights[1]

    separator_rows = [
        c[0][0]  # row arg of printer.print
        for c in printer.print.call_args_list
        if c[0][2] == "-"
    ]
    assert all(row < last_row_end for row in separator_rows), (
        "Separator was drawn below the last row"
    )


def test_single_row_no_horizontal_separator():
    """With only 1 row, no horizontal separator must be drawn."""
    w = Window(1, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="-", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c for c in printer.print.call_args_list if c[0][2] == "-"]
    assert separator_calls == []


# ---------------------------------------------------------------------------
# Corner separator (intersection)
# ---------------------------------------------------------------------------


def test_corner_separator_drawn_at_intersection():
    """At the intersection between columns and rows, a corner separator must exist."""
    w = Window(2, 2)
    for r in range(2):
        for c in range(2):
            w.set_at(r, c, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="+", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c[0] for c in printer.print.call_args_list if c[0][2] == "+"]
    # There must be at least 1 corner call (separator row + separator column)
    assert len(separator_calls) >= 1

    row_values = {c[0] for c in separator_calls}
    col_values = {c[1] for c in separator_calls}

    # There must be calls in both separator rows and separator columns
    assert len(row_values) >= 1
    assert len(col_values) >= 1


# ---------------------------------------------------------------------------
# Separator color
# ---------------------------------------------------------------------------


def test_separator_uses_default_color_by_default():
    """Without specifying a color, the separator uses Color.DEFAULT."""
    w = Window(1, 2)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(0, 1, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    for c in printer.print.call_args_list:
        if c[0][2] == "|":
            style: Style = c[0][3]
            assert style.color == Color.DEFAULT
            break


def test_separator_uses_custom_color():
    """The separator must be drawn with the specified color."""
    w = Window(1, 2)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(0, 1, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(
        10, 20, w,
        window_separator="|",
        separator_color=Color.RED,
        printer=printer,
        reader=make_reader(),
    )
    d.draw_all()

    for c in printer.print.call_args_list:
        if c[0][2] == "|":
            style: Style = c[0][3]
            assert style.color == Color.RED
            return

    pytest.fail("No separator was drawn")


def test_horizontal_separator_uses_custom_color():
    """Horizontal separator must also respect the configured color."""
    w = Window(2, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(1, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(
        10, 20, w,
        window_separator="-",
        separator_color=Color.BLUE,
        printer=printer,
        reader=make_reader(),
    )
    d.draw_all()

    for c in printer.print.call_args_list:
        if c[0][2] == "-":
            style: Style = c[0][3]
            assert style.color == Color.BLUE
            return

    pytest.fail("No horizontal separator was drawn")

# ---------------------------------------------------------------------------
# No separator: no extra calls
# ---------------------------------------------------------------------------


def test_no_separator_calls_only_content_prints():
    """With separator='', _draw_separators is not called and no separator char appears."""
    w = Window(2, 2)
    for r in range(2):
        for c in range(2):
            w.set_at(r, c, TextWidget("T", "B"))
    printer = make_printer()

    # We use a char outside the expected content to verify its absence
    d = Drawer(10, 20, w, window_separator="", printer=printer, reader=make_reader())
    d.draw_all()

    # Without a separator, there must be no calls with " " as an isolated separator
    # (we verify indirectly that _draw_separators was not invoked)
    # The number of print calls must match only the content
    total_content_cells = sum(
        (d.row_heights[r] * d.col_widths[c])
        for r in range(2)
        for c in range(2)
    )
    assert printer.print.call_count == total_content_cells