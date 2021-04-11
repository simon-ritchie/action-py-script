"""Implementations for event handler's expression scope
interfaces.
"""

import os


class HandlerScope:
    """
    Class for handler scope. This is used at with statement.
    """

    def __init__(self) -> None:
        """
        Class for handler scope. This is used at with statement.
        """

    def __enter__(self) -> None:
        """
        Enter and set event handler scope setting.
        """
        _increment_scope_count()

    def __exit__(self, *args) -> None:
        """
        Exit and remove event handler scope setting.
        """
        _decrement_scope_count()

def _increment_scope_count() -> None:
    """
    Increment current scope count.
    """
    scope_count: int = get_current_event_handler_scope_count()
    scope_count += 1
    _save_current_scope_count(count=scope_count)


def _decrement_scope_count() -> None:
    """
    Decrement current scope count.
    """
    scope_count: int = get_current_event_handler_scope_count()
    scope_count -= 1
    scope_count = max(scope_count, 0)
    _save_current_scope_count(count=scope_count)


def _save_current_scope_count(count: int) -> None:
    """
    Save current scope count.

    Parameters
    ----------
    count : int
        Scope count ot save.
    """
    from apysc.file import file_util
    from apysc.expression.expression_file_util import \
        EVENT_HANDLER_SCOPE_COUNT_FILE_PATH
    file_util.save_plain_txt(
        txt=str(count),
        file_path=EVENT_HANDLER_SCOPE_COUNT_FILE_PATH)


def get_current_event_handler_scope_count() -> int:
    """
    Get a current event handler's scope count.

    Returns
    -------
    scope_count : int
        Current event handler's scope count.
        If normal handler's call, then 1 will be returned,
        or call other handler in handler's function, then
        2 or more count will be returned.
    """
    from apysc.expression import expression_file_util
    from apysc.file import file_util
    file_path: str = expression_file_util.EVENT_HANDLER_SCOPE_COUNT_FILE_PATH
    if not os.path.isfile(file_path):
        return 0
    txt: str = file_util.read_txt(file_path=file_path)
    txt = txt.strip()
    if not txt.isdigit():
        return 0
    scope_count: int = int(txt)
    return scope_count