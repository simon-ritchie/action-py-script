"""Class implementation for graphic base class.
"""

from typing import Any

from apyscript.display.display_object import DisplayObject
from apyscript.validation import display_validation
from apyscript.validation import number_validation
from apyscript.validation import string_validation


class GraphicBase(DisplayObject):

    _variable_name: str

    def __init__(
            self, parent: Any, x: int, y: int, variable_name: str) -> None:
        """
        Vector graphic base class.

        Parameters
        ----------
        x : int
            X position.
        y : int
            Y position.
        variable_name : str
            Variable name of this instance. This will be used to
            js expression.
        """
        from apyscript.display.graphics import Graphics
        display_validation.validate_graphics(graphics=parent)
        self.parent_graphics: Graphics = parent
        number_validation.validate_integer(integer=x)
        number_validation.validate_integer(integer=y)
        self._x = x
        self._y = y
        string_validation.validate_not_empty_string(string=variable_name)
        self._variable_name = variable_name
