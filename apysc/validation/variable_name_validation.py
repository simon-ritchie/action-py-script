"""Variable name related Validation interfaces.
"""

from typing import Any

from apysc.type.variable_name_interface import VariableNameInterface


def validate_variable_name_interface_type(
        instance: Any) -> VariableNameInterface:
    """
    Validate specified instance type is VariableNameInterface.

    Parameters
    ----------
    instance : *
        Instance to be checked.

    Returns
    -------
    instance : VariableNameInterface
        Checked instance.

    Raises
    ------
    TypeError
        If specified instance type isn't VariableNameInterface.
    """
    if not isinstance(instance, VariableNameInterface):
        raise TypeError(
            'Specified instance type is not VariableNameInterface : '
            f'{type(instance)}')
    return instance
