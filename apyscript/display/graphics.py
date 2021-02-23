"""Implementations for Graphics class.
"""

from typing import Any
from typing import Optional

from apyscript.display.begin_fill_interface import BiginFillInterface
from apyscript.display.child_interface import ChildInterface
from apyscript.display.graphics_clear_interface import GraphicsClearInterface
from apyscript.display.line_style_interface import LineStyleInterface
from apyscript.display.rectangle import Rectangle
from apyscript.display.rectangle import append_draw_rect_expression
from apyscript.display.variable_name_interface import VariableNameInterface
from apyscript.expression import expression_file_util
from apyscript.expression import expression_variables_util
from apyscript.html import html_util
from apyscript.validation import display_validation


class Graphics(
        BiginFillInterface, LineStyleInterface, VariableNameInterface,
        GraphicsClearInterface, ChildInterface):

    def __init__(
            self, parent: Any,
            variable_name: Optional[str] = None) -> None:
        """
        Create a object that has each vector graphics interface.

        Parameters
        ----------
        parent : Sprite
            This instance's parent instance.
        variable_name : str or None, default None
            Variable name to set. Specified only when subclass
            instantiation.
        """
        from apyscript.display.sprite import Sprite
        display_validation.validate_sprite(sprite=parent)
        self.parent_sprite: Sprite = parent
        if variable_name is None:
            variable_name = expression_variables_util.get_next_variable_name(
                type_name='graphics')
        self.variable_name = variable_name
        self._childs = []
        self._append_constructor_expression()

    def _append_constructor_expression(self) -> None:
        """
        Append constructor expression to file.
        """
        stage_name: str = self.parent_sprite.stage.variable_name
        parent_name: str = self.parent_sprite.variable_name
        expression: str = (
            f'var {self.variable_name} = {stage_name}.group();'
            f'\n{parent_name}.add({self.variable_name});'
        )
        expression = html_util.wrap_expression_by_script_tag(
            expression=expression)
        expression_file_util.append_expression(expression=expression)

    def draw_rect(
            self, x: int, y: int, width: int, height: int) -> Rectangle:
        """
        Draw rectangle vector graphics.

        Parameters
        ----------
        x : int
            X position to start drawing.
        y : int
            Y position to start drawing.
        width : int
            Rectangle width.
        height : int
            Rectangle height.

        Returns
        -------
        rectangle : Rectangle
            Created rectangle.
        """
        rectangle: Rectangle = Rectangle(
            parent=self, x=x, y=y, width=width, height=height,
            fill_color=self.fill_color, fill_alpha=self.fill_alpha,
            line_color=self.line_color, line_thickness=self.line_thickness,
            line_alpha=self.line_alpha)
        append_draw_rect_expression(rectangle=rectangle)
        self.add_child(child=rectangle)
        return rectangle
