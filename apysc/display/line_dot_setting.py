"""Dot setting class implementation for line.
"""

from typing import Union

from apysc import Int


class LineDotSetting:

    _dot_size: Int

    def __init__(self, dot_size: Union[int, Int]) -> None:
        """
        Dot setting class for line.

        Parameters
        ----------
        dot_size : int or Int
            Dot size.
        """
        from apysc.validation import number_validation
        number_validation.validate_integer(integer=dot_size)
        if isinstance(dot_size, int):
            dot_size = Int(dot_size)
        self._dot_size = dot_size
