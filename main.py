from fash.core.cell import Style, Color
from fash.draw.drawer import Drawer
from fash.widgets.text_widget import TextWidget
from fash.windowmanager.window import Window



w = Window(2, 2)
r = TextWidget("Test", "Lorem ipsum ola!", style=Style(color=Color.RED))
g = TextWidget("Test", "Lorem ipsum ola!", style=Style(color=Color.GREEN))
b = TextWidget("Test", "Lorem ipsum ola!", style=Style(color=Color.BLUE))
y = TextWidget("Test", "Lorem ipsum ola!", style=Style(color=Color.YELLOW))
w.set_at(0, 0, r)
w.set_at(0, 1, g)
w.set_at(1, 0, b)
w.set_at(1, 1, y)

d = Drawer(25, 100, w)
d.draw_all()