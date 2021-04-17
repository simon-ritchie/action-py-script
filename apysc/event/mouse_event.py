"""Class implementation for mouse event.
"""

from typing import Generic
from typing import Optional
from typing import TypeVar

from apysc.event.event import Event
from apysc.type.variable_name_interface import VariableNameInterface
from apysc import Int

T = TypeVar('T', bound=VariableNameInterface)


class MouseEvent(Generic[T], Event):

    _this: T

    def __init__(self, this: T) -> None:
        """
        Mouse event class.

        Parameters
        ----------
        this : VariableNameInterface
            Instance that listening event (e.g., Sprite).
        """
        from apysc.expression import var_names
        super(MouseEvent, self).__init__(
            this=this, type_name=var_names.MOUSE_EVENT)

    @property
    def stage_x(self) -> Int:
        """
        Get the x-coordinate of the stage reference.

        Returns
        -------
        x : Int
            x-coordinate.
        """
        x: Int = Int(0)
        self._append_stage_x_getter_expression(x=x)
        return x

    def _append_stage_x_getter_expression(self, x: Int) -> None:
        """
        Append stage_x getter property expression to file.

        Parameters
        ----------
        x : Int
            Target x-coordinate value.
        """
        from apysc.display.stage import get_stage_element_id
        from apysc.expression import expression_file_util
        stage_elem_str: str = f'$("#{get_stage_element_id()}")'
        expression: str = (
            f'{x.variable_name} = {self.variable_name}.pageX - '
            f'{stage_elem_str}.offset().left;'
        )
        expression_file_util.append_js_expression(expression=expression)

    @property
    def stage_y(self) -> Int:
        """
        Get the y-coordinate of the stage reference.

        Returns
        -------
        y : Int
            y-coordinate.
        """
        y: Int = Int(0)
        self._append_stage_y_getter_expression(y=y)
        return y

    def _append_stage_y_getter_expression(self, y: Int) -> None:
        """
        Append stage_y getter property expression to file.

        Parameters
        ----------
        y : Int
            Target y-coordinate value.
        """
        from apysc.display.stage import get_stage_element_id
        from apysc.expression import expression_file_util
        stage_elem_str: str = f'$("#{get_stage_element_id()}")'
        expression: str = (
            f'{y.variable_name} = {self.variable_name}.pageY - '
            f'{stage_elem_str}.offset().top;'
        )
        expression_file_util.append_js_expression(expression=expression)

    @property
    def local_x(self) -> Int:
        """
        Get the x-coordinate of the event listening instance reference.
        For example, if a Sprite instance is clicked, this value will be
        x-coordinate from Sprite's left end position.

        Returns
        -------
        x : Int
            x-coordinate.
        """
        x: Int = Int(0)
        self._append_local_x_getter_expression(x=x)
        return x

    def _append_local_x_getter_expression(self, x: Int) -> None:
        """
        Append local_x getter property expression to file.

        Parameters
        ----------
        x : Int
            Target x-coordinate value.
        """
        from apysc.expression import expression_file_util
        stage_x_: Int = self.stage_x
        this: T = self.this
        expression: str = (
            f'{x.variable_name} = {stage_x_.variable_name} - '
            f'{this.variable_name}.attr("x");'
        )
        expression_file_util.append_js_expression(expression=expression)
