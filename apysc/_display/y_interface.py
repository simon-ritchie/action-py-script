"""Class implementation for the y-coordinate interface.
"""

from typing import Dict

from apysc import Int
from apysc._type.revert_interface import RevertInterface
from apysc._type.variable_name_interface import VariableNameInterface


class YInterface(VariableNameInterface, RevertInterface):

    _y: Int

    def _initialize_y_if_not_initialized(self) -> None:
        """
        Initialize _y attribute if it is not initialized yet.
        """
        if hasattr(self, '_y'):
            return
        self._y = Int(0)

    @property
    def y(self) -> Int:
        """
        Get a y-coordinate.

        Returns
        -------
        y : Int
            Y-coordinate.
        """
        from apysc._type import value_util
        self._initialize_y_if_not_initialized()
        return value_util.get_copy(value=self._y)

    @y.setter
    def y(self, value: Int) -> None:
        """
        Update y-coordinate.

        Parameters
        ----------
        value : int or Int
            Y-coordinate value.
        """
        from apysc._type.number_value_interface import NumberValueInterface
        from apysc._validation import number_validation
        if not isinstance(value, NumberValueInterface):
            number_validation.validate_integer(integer=value)
            value = Int(value=value)
        self._y = value
        self._y._append_incremental_calc_substitution_expression()
        self._append_y_update_expression()

    def _append_y_update_expression(self) -> None:
        """
        Append y position updating expression.
        """
        from apysc import append_js_expression
        from apysc._type import value_util
        self._initialize_y_if_not_initialized()
        value_str: str = value_util.get_value_str_for_expression(
            value=self._y)
        expression: str = (
            f'{self.variable_name}.y({value_str});'
        )
        append_js_expression(expression=expression)

    _y_snapshots: Dict[str, int]

    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make a value's snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not hasattr(self, '_y_snapshots'):
            self._y_snapshots = {}
        if self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._initialize_y_if_not_initialized()
        self._y_snapshots[snapshot_name] = int(self._y._value)

    def _revert(self, snapshot_name: str) -> None:
        """
        Revert a value if snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._y._value = self._y_snapshots[snapshot_name]
