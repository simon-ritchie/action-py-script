"""Class implementation for revert interface.
"""

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Tuple
from typing import Type


class RevertInterface(ABC):

    _snapshot_exists_: Dict[str, bool]

    def _initialize_ss_exists_val_if_not_initialized(self) -> None:
        """
        Initialize _snapshot_exists_ value if it is not initialized yet.
        """
        if hasattr(self, '_snapshot_exists_'):
            return
        self._snapshot_exists_ = {}

    @abstractmethod
    def _make_snapshot(self, snapshot_name: str) -> None:
        """
        Make values snapshot.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """

    @abstractmethod
    def _revert(self, snapshot_name: str) -> None:
        """
        Revert values if snapshot exists.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """

    def _run_all_make_snapshot_methods(self, snapshot_name: str) -> None:
        """
        Run all _make_snapshot methods. If instance is multiple
        inheritance one, and each has RevertInterface, then each
        _make_snapshot methods will be called.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self_type: Type = type(self)
        self._run_base_cls_make_snapshot_methods_recursively(
            class_=self_type, snapshot_name=snapshot_name)
        self._set_snapshot_exists_val(snapshot_name=snapshot_name)

    def _run_base_cls_make_snapshot_methods_recursively(
            self, class_: Type, snapshot_name: str) -> None:
        """
        Run base classes make_snapshot methods recursively.

        Parameters
        ----------
        class_ : type
            Target type.
        snapshot_name : str
            Target snapshot name.
        """
        base_classes: Tuple[Type, ...] = class_.__bases__
        for base_class in base_classes:
            if not issubclass(base_class, RevertInterface):
                continue
            base_class._make_snapshot(self, snapshot_name)
            self._run_base_cls_make_snapshot_methods_recursively(
                class_=base_class, snapshot_name=snapshot_name)
        class_._make_snapshot(self, snapshot_name=snapshot_name)

    def _run_all_revert_methods(self, snapshot_name: str) -> None:
        """
        Run all _revert methods. If instance is multiple inheritance one,
        and each has RevertInterface, then each _revert methods will be
        called.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self_type: Type = type(self)
        self._run_base_cls_revert_methods_recursively(
            class_=self_type, snapshot_name=snapshot_name)
        self._delete_snapshot_exists_val(snapshot_name=snapshot_name)

    def _run_base_cls_revert_methods_recursively(
            self, class_: Type, snapshot_name: str) -> None:
        """
        Run base classes revert methods recursively.

        Parameters
        ----------
        class_ : type
            Target type.
        snapshot_name : str
            Target snapshot name.
        """
        base_classes: Tuple[Type, ...] = class_.__bases__
        for base_class in base_classes:
            if not issubclass(base_class, RevertInterface):
                continue
            base_class._revert(self, snapshot_name=snapshot_name)
            self._run_base_cls_revert_methods_recursively(
                class_=base_class, snapshot_name=snapshot_name)
        class_._revert(self, snapshot_name=snapshot_name)

    def _snapshot_exists(self, snapshot_name: str) -> bool:
        """
        Get a boolean value whether snapshot value exists or not.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.

        Returns
        -------
        snapshot_exists : bool
            Boolean value whether snapshot value exists or not.
        """
        self._initialize_ss_exists_val_if_not_initialized()
        return snapshot_name in self._snapshot_exists_

    def _set_snapshot_exists_val(self, snapshot_name: str) -> None:
        """
        Set boolean value whether snapshot value exists or not.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._initialize_ss_exists_val_if_not_initialized()
        self._snapshot_exists_[snapshot_name] = True

    def _delete_snapshot_exists_val(self, snapshot_name: str) -> None:
        """
        Delete boolean value whether snapshot value exists or not.

        Parameters
        ----------
        snapshot_name : str
            Target snapshot name.
        """
        self._initialize_ss_exists_val_if_not_initialized()
        if snapshot_name in self._snapshot_exists_:
            del self._snapshot_exists_[snapshot_name]

    def _get_next_snapshot_name(self) -> str:
        """
        Get a next snapshot name.

        Returns
        -------
        snapshot_name : str
            Next snapshot name.
        """
        from apysc.expression import expression_variables_util
        from apysc.expression.var_names import SNAPSHOT
        snapshot_name: str = expression_variables_util.get_next_variable_name(
            type_name=SNAPSHOT)
        return snapshot_name
