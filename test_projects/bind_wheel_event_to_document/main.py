"""Test project for bind_wheel_event_to_document interface.

Command examples:
$ python test_projects/bind_wheel_event_to_document/main.py
$ python bind_wheel_event_to_document/main.py
"""

import sys
from typing import Any
from typing import Dict

sys.path.append('./')

import os
from types import ModuleType

import apysc as ap
from apysc._file import file_util

this_module: ModuleType = sys.modules[__name__]

_DEST_DIR_PATH: str = os.path.join(
    file_util.get_abs_module_dir_path(module=this_module),
    'test_output/'
)


def main() -> None:
    """
    Entry point of this test project.
    """
    _: ap.Stage = ap.Stage(
        background_color='#111',
        stage_width=1000, stage_height=500)
    ap.bind_wheel_event_to_document(
        handler=on_document_wheel, options={'msg': 'Hello!'})

    ap.save_overall_html(dest_dir_path=_DEST_DIR_PATH)


def on_document_wheel(e: ap.WheelEvent, options: Dict[str, Any]) -> None:
    """
    Test handler that called when wheeled on document.

    Parameters
    ----------
    e : WheelEvent
        Event object.
    options : dict
        Optional arguments dictionary.
    """
    ap.trace('Wheeled!')
    ap.trace('delta_x:', e.delta_x)
    ap.trace('delta_y:', e.delta_y)
    ap.assert_equal(expected='Hello!', actual=options['msg'])


if __name__ == '__main__':
    main()
