from enum import Enum
from dataclasses import dataclass, field

class Color(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"

@dataclass
class Style:
    bold: bool = False
    color: Color | None = None


@dataclass
class Cell:
    char: str = " "
    style: Style = field(default_factory=Style)

    def __str__(self) -> str:
        return self.char
