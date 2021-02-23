"""Parent related validation interfaces.
"""

from typing import Any
from typing import Optional


def validate_parent_instance(parent: Optional[Any]) -> None:
    """
    Validate specified parent is `ChildInterface` instance.

    Parameters
    ----------
    parent : *
        Any parent instance or None.

    Raises
    ------
    ValueError
        If specified parent is not None and not `ChildInterface`
        instance.
    """
    if parent is None:
        return
    from apyscript.display.child_interface import ChildInterface
    if isinstance(parent, ChildInterface):
        return
    raise ValueError(
        'Specified parent is not None and not `ChildInterface` instance,'
        f' like a Sprite: {type(parent)}')


def validate_parent_contains_child(
        parent: Optional[Any], child: Any) -> None:
    """
    Validate parent contains specified child.

    Parameters
    ----------
    parent : ChildInterface or None
        Parent instance.
    child : DisplayObject
        Child instance.

    Raises
    ------
    ValueError
        If parent not contains specified child. If parent is None,
        check will be skipped.
    """
    from apyscript.display.child_interface import ChildInterface
    from apyscript.display.display_object import DisplayObject
    parent_: Optional[ChildInterface] = parent
    child_: DisplayObject = child
    if parent_ is None:
        return
    if parent_.contains(child=child_):
        return
    raise ValueError(
        'Parent not containts specified child.'
        f'\nParent type: {type(parent_)}'
        f'\nChild type: {type(child_)}'
        f'\nChild name: {child_.variable_name}')
