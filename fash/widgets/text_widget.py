class TextWidget:
    def __init__(self, title, text) -> None:
        pass

    def draw(self, max_w, max_h) -> str:
        return (("*" * max_w) + "\n") * max_h
