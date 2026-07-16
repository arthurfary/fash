class InvalidCharacterLengthError(ValueError):
    """
    The informed character had an invalid lenght.
    Possible causes are not passing required parameters or using longer strings for single chars.
    """
    ...

class CursorPositionError(RuntimeError):
    """Reader module could not determine the cursor position in the output device."""
    ...

class WidgetOutOfBoundsError(IndexError):
    """
    Raised when attempting to access a widget that is non existing or outside grid size.
    Windows are 0-indexed so the last valid widget in a 3 sized grid is index 2
    """
    ...