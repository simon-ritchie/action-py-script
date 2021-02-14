"""Class implementation for begin_fill method related interface.
"""


from typing import Optional

from apyscript.color import color_util
from apyscript.validation import color_validation


class BiginFillInterface:

    _fill_color: Optional[str] = None
    _fill_alpha: Optional[float] = None

    def begin_fill(self, color: str, alpha: float = 1.0) -> None:
        """
        Set single color value for fill.

        Parameters
        ----------
        color : str
            Hexadecimal color string. e.g., '#00aaff'
        alpha : float, default 1.0
            Color opacity (0.0 to 1.0).
        """
        color = color_util.complement_hex_color(hex_color_code=color)
        self._fill_color = color
        color_validation.validate_alpha_range(alpha=alpha)
        self._fill_alpha = alpha

    @property
    def fill_color(self) -> Optional[str]:
        """
        Get current fill color.

        Returns
        -------
        fill_color : str or None
            Current fill color (hexadecimal string, e.g., '#00aaff').
            If not be set, None will be returned.
        """
        return self._fill_color

    @property
    def fill_alpha(self) -> Optional[float]:
        """
        Get current fill color opacity.

        Returns
        -------
        fill_alpha : float or None
            Current fill color opacity (0.0 to 1.0).
            If not be set, None will be returned.
        """
        return self._fill_alpha