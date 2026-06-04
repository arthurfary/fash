from fash.draw import drawer
from fash.widgets.text_widget import TextWidget
from fash.windowmanager import window


base = window.Window()

base.make_grid(3, 3)

# base.get_at(2, 2)

base.set_at(2, 2, TextWidget("teste", "teste2"))

d = drawer.Drawer(base)

d.draw_all()
