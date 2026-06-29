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
# Validação do construtor
# ---------------------------------------------------------------------------


def test_separator_empty_string_is_valid():
    """Separador vazio é permitido."""
    d = make_drawer(separator="")
    assert d.window_separator == ""


def test_separator_single_char_is_valid():
    """Separador de 1 caractere é permitido."""
    d = make_drawer(separator="|")
    assert d.window_separator == "|"


def test_separator_two_chars_raises():
    """Separador com 2+ caracteres deve lançar ValueError."""
    with pytest.raises(ValueError):
        make_drawer(separator="||")


def test_separator_long_string_raises():
    """String longa deve lançar ValueError."""
    with pytest.raises(ValueError):
        make_drawer(separator="---")


# ---------------------------------------------------------------------------
# Separador vertical (entre colunas)
# ---------------------------------------------------------------------------


def test_vertical_separator_drawn_between_columns():
    """O caractere separador deve aparecer na coluna logo após o conteúdo."""
    w = Window(1, 2)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(0, 1, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    printed_chars = [c[0][2] for c in printer.print.call_args_list]
    assert "|" in printed_chars


def test_vertical_separator_not_drawn_after_last_column():
    """O separador NÃO deve ser desenhado após a última coluna."""
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
        c[0][1]  # col arg do printer.print
        for c in printer.print.call_args_list
        if c[0][2] == "|"
    ]
    assert all(col < last_col_end for col in separator_cols), (
        "Separador foi desenhado além da última coluna"
    )


def test_single_column_no_vertical_separator():
    """Com apenas 1 coluna, nenhum separador vertical deve ser desenhado."""
    w = Window(1, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="|", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c for c in printer.print.call_args_list if c[0][2] == "|"]
    assert separator_calls == []


# ---------------------------------------------------------------------------
# Separador horizontal (entre linhas)
# ---------------------------------------------------------------------------


def test_horizontal_separator_drawn_between_rows():
    """O caractere separador deve aparecer na linha logo após o conteúdo."""
    w = Window(2, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    w.set_at(1, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="-", printer=printer, reader=make_reader())
    d.draw_all()

    printed_chars = [c[0][2] for c in printer.print.call_args_list]
    assert "-" in printed_chars


def test_horizontal_separator_not_drawn_after_last_row():
    """O separador NÃO deve ser desenhado após a última linha."""
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
        c[0][0]  # row arg do printer.print
        for c in printer.print.call_args_list
        if c[0][2] == "-"
    ]
    assert all(row < last_row_end for row in separator_rows), (
        "Separador foi desenhado abaixo da última linha"
    )


def test_single_row_no_horizontal_separator():
    """Com apenas 1 linha, nenhum separador horizontal deve ser desenhado."""
    w = Window(1, 1)
    w.set_at(0, 0, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="-", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c for c in printer.print.call_args_list if c[0][2] == "-"]
    assert separator_calls == []


# ---------------------------------------------------------------------------
# Separador de canto (interseção)
# ---------------------------------------------------------------------------


def test_corner_separator_drawn_at_intersection():
    """Na interseção entre colunas e linhas, um separador de canto deve existir."""
    w = Window(2, 2)
    for r in range(2):
        for c in range(2):
            w.set_at(r, c, TextWidget("T", "B"))
    printer = make_printer()

    d = Drawer(10, 20, w, window_separator="+", printer=printer, reader=make_reader())
    d.draw_all()

    separator_calls = [c[0] for c in printer.print.call_args_list if c[0][2] == "+"]
    # Deve haver ao menos 1 chamada de canto (linha de sep + coluna de sep)
    assert len(separator_calls) >= 1

    row_values = {c[0] for c in separator_calls}
    col_values = {c[1] for c in separator_calls}

    # Deve existir chamadas tanto em linhas quanto colunas de separador
    assert len(row_values) >= 1
    assert len(col_values) >= 1


# ---------------------------------------------------------------------------
# Cor do separador
# ---------------------------------------------------------------------------


def test_separator_uses_default_color_by_default():
    """Sem especificar cor, o separador usa Color.DEFAULT."""
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
    """O separador deve ser desenhado com a cor especificada."""
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

    pytest.fail("Nenhum separador foi desenhado")


def test_horizontal_separator_uses_custom_color():
    """Separador horizontal também deve respeitar a cor configurada."""
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

    pytest.fail("Nenhum separador horizontal foi desenhado")

# ---------------------------------------------------------------------------
# Sem separador: nenhuma chamada extra
# ---------------------------------------------------------------------------


def test_no_separator_calls_only_content_prints():
    """Com separator='', _draw_separators não é chamado e nenhum char de sep aparece."""
    w = Window(2, 2)
    for r in range(2):
        for c in range(2):
            w.set_at(r, c, TextWidget("T", "B"))
    printer = make_printer()

    # Usamos um char fora do conteúdo esperado para verificar ausência
    d = Drawer(10, 20, w, window_separator="", printer=printer, reader=make_reader())
    d.draw_all()

    # Sem separador, não deve haver nenhuma chamada com " " como separador isolado
    # (verificamos indiretamente que _draw_separators não foi invocado)
    # O número de print calls deve ser apenas o do conteúdo
    total_content_cells = sum(
        (d.row_heights[r] * d.col_widths[c])
        for r in range(2)
        for c in range(2)
    )
    assert printer.print.call_count == total_content_cells