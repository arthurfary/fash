from fash.draw.drawer import Drawer
from fash.windowmanager.window import Window


root_win = Window(2, 2)

root_win.set_at(0, 0, "test")

drawer = Drawer(8, 30, root_win)

drawer.draw_all()
