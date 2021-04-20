"""Class implementation for double click interface.
"""

from typing import Any
from typing import Dict
from typing import Optional

from apysc.event.handler import Handler
from apysc.event.handler import HandlerData
from apysc.event.event_interface_base import EventInterfaceBase


class DoubleClickInterface(EventInterfaceBase):

    _dbclick_handlers: Dict[str, HandlerData]

    def dblclick(
            self, handler: Handler,
            kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Add double click event listener setting.

        Parameters
        ----------
        handler : Handler
            Callable that called when this instance is double clicked.
        kwargs : dict or None, default None
            Keyword arguments to be passed to handler.

        Returns
        -------
        name : str
            Handler's name.
        """
        from apysc import MouseEvent
        from apysc.event.handler import append_handler_expression
        from apysc.event.handler import get_handler_name
        from apysc.type.variable_name_interface import VariableNameInterface
        self_instance: VariableNameInterface = \
            self.validate_self_is_variable_name_interface()
        self._initialize_dbclick_handlers_if_not_initialized()
        pass

    def _initialize_dbclick_handlers_if_not_initialized(self) -> None:
        """
        Initialize _dbclick_handlers attribute if it is not
        initialized yet.
        """
        if hasattr(self, '_dbclick_handlers'):
            return
        self._dbclick_handlers = {}
