"""Test project for same handler's multiple event binding case.

Command examples:
$ python test_projects/event_multiple_binding/main.py
$ python event_multiple_binding/main.py
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
    stage: ap.Stage = ap.Stage(
        background_color='#111',
        stage_width=1000, stage_height=500)
    int_1: ap.Int = ap.Int(10)
    stage.click(on_click, options={'int_val': int_1})
    sprite_1: ap.Sprite = ap.Sprite(stage=stage)
    int_2: ap.Int = ap.Int(20)
    sprite_1.click(on_click, options={'int_val': int_2})
    sprite_1.graphics.begin_fill(color='#0af')
    sprite_1.graphics.draw_rect(x=50, y=50, width=50, height=50)

    ap.save_overall_html(dest_dir_path=_DEST_DIR_PATH)


def on_click(e: ap.MouseEvent, options: Dict[str, Any]) -> None:
    """
    Test handler that called when object is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event object.
    options : dict
        Optional arguments dictionary.
    """
    ap.trace('-' * 20)
    ap.trace(
        'clicked! Integer value is:', options['int_val'],
        ', this instance\'s type:', type(e.this))
    if isinstance(e.this, ap.Stage):
        ap.assert_equal(expected=10, actual=options['int_val'])
        return
    if isinstance(e.this, ap.Sprite):
        ap.assert_equal(expected=20, actual=options['int_val'])
        return


if __name__ == '__main__':
    main()
