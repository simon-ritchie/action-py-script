"""`trace` (console.log expression) interface implementations
"""

from typing import Any
from typing import List

from apyscript.display.variable_name_interface import VariableNameInterface
from apyscript.expression import expression_file_util
from apyscript.html import html_util


def trace(*args: Any) -> None:
    """
    Display arguments information to console. This function will
    save js `console.log` expression.

    Parameters
    ----------
    *args : list
        Any arguments to display to console.
    """
    expression: str = 'console.log('
    arg_strs: List[str] = []
    for arg in args:
        if isinstance(arg, VariableNameInterface):
            arg_strs.append(f'{arg.variable_name}')
            continue
        arg_strs.append(f'"{str(arg)}"')
    expression += ', '.join(arg_strs)
    expression += ');'
    expression = html_util.wrap_expression_by_script_tag(
        expression=expression)
    expression_file_util.append_expression(expression=expression)
