from fash.draw.ansi import AnsiFormatter
from fash.draw.drawer import Drawer
import pytest
import re
from fash.widgets.base_widget import Widget
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


@pytest.fixture
def empty_window():
    return Window(2, 2)


@pytest.fixture
def lorem_ipsum_window(empty_window):
    x = TextWidget("Test", LOREM_IPSUM)
    empty_window.set_at(0, 0, x)
    empty_window.set_at(0, 1, x)
    empty_window.set_at(1, 0, x)
    empty_window.set_at(1, 1, x)
    return empty_window


def test_window_instanciable(empty_window):
    assert isinstance(empty_window, Window)


def test_add_widgets_to_grid(lorem_ipsum_window):
    widget: Widget | None = lorem_ipsum_window.get_at(1, 1)
    assert widget is not None and isinstance(widget, TextWidget)


def test_drawer(lorem_ipsum_window, capsys):
    my_drawer = Drawer(25, 100, lorem_ipsum_window)

    my_drawer.draw_all()

    captured = capsys.readouterr()

    assert captured is not None and len(captured) > 0
    clean = AnsiFormatter.strip_ansi(captured.out).replace("\n", "")

    assert "Lorem ipsum" in clean

