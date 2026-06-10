from abc import abstractmethod


class Widget:
    """
    Widget class
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self, max_width, max_height) -> str:
        """
        Function that handles the displaying of the widget.

        Returns a formatted string, must be set between the bouderies of `max_height` and `max_height`
        """
