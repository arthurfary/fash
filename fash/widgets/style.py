"""Style options shared by the ready-made widgets."""

from typing import TypedDict

from fash.core.cell import Color


class WidgetStyle(TypedDict, total=False):
    color: Color | None