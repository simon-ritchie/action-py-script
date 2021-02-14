"""Class implementation for line color interface.
"""

from typing import Optional

from apyscript.color import color_util
from apyscript.display.variable_name_interface import VariableNameInterface
from apyscript.expression import expression_file_util
from apyscript.html import html_util


class LineColorInterface(VariableNameInterface):

    _line_color: Optional[str] = None

    @property
    def line_color(self) -> Optional[str]:
        """
        Get this instance's line color.

        Returns
        -------
        line_color : str or None
            Current line color (hexadecimal string, e.g., '#00aaff').
            If not be set, None will be returned.
        """
        return self._line_color

    @line_color.setter
    def line_color(self, value: str) -> None:
        """
        Update this instance's line color.

        Parameters
        ----------
        value : str
            Line color to set.
        """
        value = color_util.complement_hex_color(hex_color_code=value)
        self._line_color = value
