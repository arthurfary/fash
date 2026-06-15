from dataclasses import dataclass, field


@dataclass
class Style:
    bold: bool = False


@dataclass
class Cell:
    char: str = " "
    style: Style = field(default_factory=Style)

    def __str__(self) -> str:
        return self.char
