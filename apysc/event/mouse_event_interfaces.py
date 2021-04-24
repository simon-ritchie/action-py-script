"""Class implementation for inheritance of each mouse event interfaces.
"""

from apysc.event.click_interface import ClickInterface
from apysc.event.double_click_interface import DoubleClickInterface
from apysc.event.mouse_down_interface import MouseDownInterface
from apysc.event.mouse_up_interface import MouseUpInterface
from apysc.event.mouse_over_interface import MouseOverInterface


class MouseEventInterfaces(
        ClickInterface, DoubleClickInterface, MouseDownInterface,
        MouseUpInterface, MouseOverInterface):
    """Class implementation for inheritance of each mouse event interfaces.
    """
