from fash.core.cell import Color
from fash.draw.styles import ANSI_COLOR_MAP, ANSI_RESET
from fash.draw.drawer import Drawer
import pytest
import re
from fash.widgets.text_widget import TextWidget, TextWidgetStyle
from fash.windowmanager.window import Window

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


def strip_ansi(text: str) -> str:
    return re.sub(r'\x1b\[[^A-Za-z]*[A-Za-z]', '', text)

@pytest.fixture
def empty_window():
    return Window(2, 2)

@pytest.fixture
def colored_window(empty_window):
    r = TextWidget("Test", LOREM_IPSUM, style=TextWidgetStyle(Color.RED))
    g = TextWidget("Test", LOREM_IPSUM, style=TextWidgetStyle(Color.GREEN))
    b = TextWidget("Test", LOREM_IPSUM, style=TextWidgetStyle(Color.BLUE))
    y = TextWidget("Test", LOREM_IPSUM, style=TextWidgetStyle(Color.YELLOW))
    empty_window.set_at(0, 0, r)
    empty_window.set_at(0, 1, g)
    empty_window.set_at(1, 0, b)
    empty_window.set_at(1, 1, y)
    return empty_window

@pytest.fixture
def red_and_white_window(empty_window):
    r = TextWidget("Test", LOREM_IPSUM, style=TextWidgetStyle(Color.RED))
    w = TextWidget("Test", LOREM_IPSUM)
    empty_window.set_at(0, 0, r)
    empty_window.set_at(0, 1, w)
    empty_window.set_at(1, 0, w)
    empty_window.set_at(1, 1, r)
    return empty_window

@pytest.fixture
def plain_window(empty_window):
    w = TextWidget("Test", LOREM_IPSUM)
    empty_window.set_at(0, 0, w)
    empty_window.set_at(0, 1, w)
    empty_window.set_at(1, 0, w)
    empty_window.set_at(1, 1, w)
    return empty_window

def test_colors_rgby(colored_window, capsys):
    Drawer(25, 100, colored_window).draw_all()
    output = capsys.readouterr().out
    assert ANSI_COLOR_MAP[Color.RED] in output
    assert ANSI_COLOR_MAP[Color.GREEN] in output
    assert ANSI_COLOR_MAP[Color.BLUE] in output
    assert ANSI_COLOR_MAP[Color.YELLOW] in output

def test_reset_color(red_and_white_window, capsys):
    Drawer(25, 100, red_and_white_window).draw_all()
    output = capsys.readouterr().out
    assert ANSI_COLOR_MAP[Color.RED] in output
    assert ANSI_RESET in output

    assert output.count(ANSI_RESET) == output.count(ANSI_COLOR_MAP[Color.RED])

def test_no_color_window_does_not_emit_color_codes(plain_window, capsys):
    Drawer(25, 100, plain_window).draw_all()
    output = capsys.readouterr().out
    assert ANSI_RESET not in output
    assert all(code not in output for code in ANSI_COLOR_MAP.values())

def test_color_reset_count_for_all_colors(colored_window, capsys):
    Drawer(25, 100, colored_window).draw_all()
    output = capsys.readouterr().out
    total_color_codes = sum(output.count(code) for code in ANSI_COLOR_MAP.values())
    assert total_color_codes > 0
    assert output.count(ANSI_RESET) == total_color_codes

def test_ansi_color_map_values_are_valid():
    assert all(isinstance(code, str) and code.startswith("\033[") and code.endswith("m") for code in ANSI_COLOR_MAP.values())

    