"""Class implementation for line dot setting interface.
"""

from typing import Any, Optional
from typing import Dict
from typing import Union

from apysc.type.revert_interface import RevertInterface
from apysc.type.variable_name_interface import VariableNameInterface
from apysc.display.line_dot_setting import LineDotSetting


class LineDotSettingInterface(VariableNameInterface, RevertInterface):

    _line_dot_setting: Optional[LineDotSetting]

    def _initialize_line_dot_setting_if_not_initialized(self) -> None:
        """
        Initialize _line_dot_setting attribute if it is not
        initialized yet.
        """
        if hasattr(self, '_line_dot_setting'):
            return
        self._line_dot_setting = None

    @property
    def line_dot_setting(self) -> Optional[LineDotSetting]:
        """
        Get this instance's line dot setting.

        Returns
        -------
        line_dot_setting : LineDotSetting or None
            Lien dot setting.
        """
        self._initialize_line_dot_setting_if_not_initialized()
        return self._line_dot_setting

    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make values' snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """

    def _revert(self, snapshot_name: str) -> None:
        """
        Revert values if snapshots exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
