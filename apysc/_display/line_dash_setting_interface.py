"""Class implementation for line dash setting interface.
"""

from typing import Dict
from typing import Optional

from apysc._display.line_dash_setting import LineDashSetting
from apysc._type.revert_interface import RevertInterface
from apysc._type.variable_name_interface import VariableNameInterface


class LineDashSettingInterface(VariableNameInterface, RevertInterface):

    _line_dash_setting: Optional[LineDashSetting]

    def _initialize_line_dash_setting_if_not_initialized(self) -> None:
        """
        Initialize _line_dash_setting attribute if it is not
        initialized yet.
        """
        if hasattr(self, '_line_dash_setting'):
            return
        self._line_dash_setting = None

    @property
    def line_dash_setting(self) -> Optional[LineDashSetting]:
        """
        Get current line dash setting.

        Returns
        -------
        line_dash_setting : LineDashSetting or None
            Line dash setting.
        """
        self._initialize_line_dash_setting_if_not_initialized()
        return self._line_dash_setting

    @line_dash_setting.setter
    def line_dash_setting(self, value: Optional[LineDashSetting]) -> None:
        """
        Set line dash setting.

        Parameters
        ----------
        value : LineDashSetting or None
            Line dash setting to set.
        """
        from apysc._validation import display_validation
        self._update_line_dash_setting_and_skip_appending_exp(value=value)
        self._append_line_dash_setting_update_expression()
        display_validation.validate_multiple_line_settings_isnt_set(
            any_instance=self)

    def _update_line_dash_setting_and_skip_appending_exp(
            self, value: Optional[LineDashSetting]) -> None:
        """
        Update line dash setting and skip appending expression to file.

        Parameters
        ----------
        value : LineDashSetting or None
            Line dash setting to set.
        """
        if value is not None and not isinstance(value, LineDashSetting):
            raise TypeError(
                'Not supported line_dash_setting type specified: '
                f'{type(value)}'
                '\nAcceptable ones are: LineDashSetting or None.')
        self._line_dash_setting = value

    def _append_line_dash_setting_update_expression(self) -> None:
        """
        Append line dash setting updating expression to file.
        """
        from apysc import append_js_expression
        if self._line_dash_setting is None:
            setting_str: str = '""'
        else:
            setting_str = (
                f'String({self._line_dash_setting.dash_size.variable_name})'
                ' + " " + '
                f'String({self._line_dash_setting.space_size.variable_name})'
            )
        expression: str = (
            f'{self.variable_name}.css("stroke-dasharray", {setting_str});'
        )
        append_js_expression(expression=expression)

    _line_dash_setting_snapshots: Dict[str, Optional[LineDashSetting]]

    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make value's snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not hasattr(self, '_line_dash_setting_snapshots'):
            self._line_dash_setting_snapshots = {}
        if self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._initialize_line_dash_setting_if_not_initialized()
        self._line_dash_setting_snapshots[snapshot_name] = \
            self._line_dash_setting

    def _revert(self, snapshot_name: str) -> None:
        """
        Revert value if snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        if not self._snapshot_exists(snapshot_name=snapshot_name):
            return
        self._line_dash_setting = self._line_dash_setting_snapshots[
            snapshot_name]
