from fash.widgets.base_widget import Widget
import textwrap


class TextWidget(Widget):
    def __init__(self, title: str, text: str) -> None:
        self.title = title
        self.text = text
        self.PADDING_CHAR = "."

    def draw(self, max_width, max_height) -> str:
        out_str = self.title.center(max_width, self.PADDING_CHAR) + "\n"
        out_str = textwrap.fill(
            out_str + self.text,
            max_width,
            max_lines=max_height,
        )

        return out_str
