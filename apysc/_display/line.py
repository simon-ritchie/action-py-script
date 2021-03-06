"""Implementations of Line class.
"""

from typing import Any

from apysc._display.line_base import LineBase

_Graphics = Any
_Point2D = Any


class Line(LineBase):

    _start_point: _Point2D
    _end_point: _Point2D

    def __init__(
            self, parent: _Graphics,
            start_point: _Point2D,
            end_point: _Point2D) -> None:
        """
        Create a line vector graphics.

        Parameters
        ----------
        parent : Graphics
            Graphics instance to link this graphic.
        start_point : Points2D
            Line start point.
        end_point : Points2D
            Line end point.
        """
        from apysc._display.graphics import Graphics
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names
        from apysc._validation import geom_validation
        geom_validation.validate_point_2d_type(point=start_point)
        geom_validation.validate_point_2d_type(point=end_point)
        parent_graphics: Graphics = parent
        variable_name: str = expression_variables_util.get_next_variable_name(
            type_name=var_names.LINE)
        super(Line, self).__init__(
            parent=parent, x=0, y=0, variable_name=variable_name)
        self._start_point = start_point
        self._end_point = end_point
        self._set_initial_basic_values(parent=parent)
        self._append_constructor_expression()
        self._set_line_setting_if_not_none_value_exists(
            parent_graphics=parent_graphics)

    def _append_constructor_expression(self) -> None:
        """
        Append constructor expression to file.
        """
        from apysc import append_js_expression
        from apysc._display.stage import get_stage_variable_name
        stage_variable_name: str = get_stage_variable_name()
        points_str: str = self._make_points_expression()
        expression: str = (
            f'var {self.variable_name} = {stage_variable_name}'
            f'\n  .line({points_str})'
            '\n  .attr({'
        )
        expression = self._append_basic_vals_expression(
            expression=expression,
            indent_num=2)
        expression = self._append_basic_vals_expression(
            expression=expression, indent_num=2)
        expression += '\n  });'
        append_js_expression(expression=expression)

    def _make_points_expression(self) -> str:
        """
        Make line start and end expression str.

        Returns
        -------
        expression : str
            Each points expression.
        """
        from apysc import Point2D
        start_point: Point2D = self._start_point
        end_point: Point2D = self._end_point
        expression: str = (
            f'{start_point.x.variable_name}, '
            f'{start_point.y.variable_name}, '
            f'{end_point.x.variable_name}, '
            f'{end_point.y.variable_name}'
        )
        return expression

    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).

        Returns
        -------
        repr_str : str
            Type name and variable name will be set
            (e.g., `Line('<variable_name>')`).
        """
        repr_str: str = f"Line('{self.variable_name}')"
        return repr_str
