import pytest
from fash.core.cell import Color, Style
from fash.draw.ansi import AnsiFormatter
from fash.draw.printer import Printer

# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def printer():
    return Printer()


# ── Helpers ────────────────────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD_ON = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"


def out(capsys) -> str:
    return capsys.readouterr().out


# ── Testes ─────────────────────────────────────────────────────────────────────


class TestPrint:
    def test_cursor_position_in_output(self, printer, capsys):
        printer.print(3, 7, "C")
        assert out(capsys).startswith(AnsiFormatter.move_cursor(3, 7))

    @pytest.mark.parametrize("row,col", [(0, 0), (5, 3), (10, 20)])
    def test_cursor_position_parametrized(self, printer, capsys, row, col):
        printer.print(row, col, "P")
        assert out(capsys).startswith(AnsiFormatter.move_cursor(row, col))

    def test_no_style_produces_no_ansi(self, printer, capsys):
        printer.print(0, 0, "A")
        output = out(capsys)
        assert output == AnsiFormatter.move_cursor(0, 0) + "A"

    def test_color_applied(self, printer, capsys):
        printer.print(0, 0, "X", Style(color=Color.RED))
        output = out(capsys)
        assert RED in output
        assert RESET in output

    def test_bold_applied(self, printer, capsys):
        printer.print(0, 0, "B", Style(bold=True))
        output = out(capsys)
        assert BOLD_ON in output
        assert RESET in output

    def test_color_and_bold_applied(self, printer, capsys):
        printer.print(0, 0, "Z", Style(bold=True, color=Color.GREEN))
        output = out(capsys)
        assert GREEN in output
        assert BOLD_ON in output
        assert RESET in output

    @pytest.mark.parametrize(
        "color,code",
        [
            (Color.RED, RED),
            (Color.GREEN, GREEN),
            (Color.BLUE, BLUE),
            (Color.YELLOW, YELLOW),
        ],
    )
    def test_all_colors(self, printer, capsys, color, code):
        printer.print(0, 0, "X", Style(color=color))
        output = out(capsys)
        assert code in output
        assert RESET in output

    def test_consecutive_calls_are_independent(self, printer, capsys):
        printer.print(0, 0, "A", Style(bold=True))
        first = out(capsys)
        printer.print(0, 1, "B")
        second = out(capsys)
        assert RESET in first
        assert RESET not in second
        assert BOLD_ON not in second

