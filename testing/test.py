# run with python -m testing.test
from fash.draw.drawer import Drawer
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window

my_win = Window(2, 2)

x = TextWidget(
    "Test",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
)

my_win.set_at(0, 0, x)
my_win.set_at(0, 1, x)
my_win.set_at(1, 0, x)
my_win.set_at(1, 1, x)

# print(my_win)
# print(my_win.get_at(0, 0))

my_drawer = Drawer(25, 100, my_win)

my_drawer.draw_all()
