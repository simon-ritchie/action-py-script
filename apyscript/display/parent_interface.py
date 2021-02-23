"""Class implementation for parent related interface.
"""

from typing import Any
from typing import Optional

from apyscript.validation import parent_validation


class ParentInterface:

    _parent: Optional[Any] = None

    @property
    def parent(self) -> Optional[Any]:
        """
        Get parent instance that has a add_child and remove_child
        interfaces.

        Returns
        -------
        parent : any parent instance or None
            Parent instance that has a add_child and remove_child
            interfaces. If this instance not have parent instance (not
            added child), None will be returned.
        """
        return self._parent

    @parent.setter
    def parent(self, value: Optional[Any]) -> None:
        """
        Set parent instance.

        Notes
        -----
        Only use this setter method at add_child or that's related
        interface.

        Parameters
        ----------
        value : *
            Parent instance to be set.

        Raises
        ------
        ValueError
            If specified instance is not None and hasn't `ChildInterface`
            interfaces.
        """
        parent_validation.validate_parent_instance(parent=value)
        parent_validation.validate_parent_contains_child(
            parent=value, child=self)
        self._parent = value

    def remove_from_parent(self) -> None:
        """
        Remove this instance from parent.

        Raises
        ------
        ValueError
            If this instance is not added to any parent.
        """
        if self._parent is None:
            raise ValueError(
                'This instance is not added to any parent.')
        from apyscript.display.child_interface import ChildInterface
        from apyscript.display.display_object import DisplayObject
        parent: ChildInterface = self._parent
        child: DisplayObject = self  # type: ignore
        parent.remove_child(child=child)
