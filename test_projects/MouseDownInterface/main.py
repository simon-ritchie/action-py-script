"""Test project for MouseDownInterface class.

Command examples:
$ python test_projects/MouseDownInterface/main.py
$ python MouseDownInterface/main.py
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
    """Entry point of this test project.
    """
    stage: ap.Stage = ap.Stage(
        background_color='#111',
        stage_width=1000, stage_height=500)
    sprite_1: ap.Sprite = ap.Sprite(stage=stage)
    sprite_1.graphics.begin_fill(color='#0af')

    rectangle_1: ap.Rectangle = sprite_1.graphics.draw_rect(
        x=50, y=50, width=50, height=50)
    rectangle_1.mousedown(
        handler=on_rectangle_1_mouse_down,
        options={'msg': 'Hello!'})

    rectangle_2: ap.Rectangle = sprite_1.graphics.draw_rect(
        x=150, y=50, width=50, height=50)
    rectangle_2.mousedown(handler=on_rectangle_2_mouse_down)
    rectangle_2.unbind_mousedown(handler=on_rectangle_2_mouse_down)

    rectangle_3: ap.Rectangle = sprite_1.graphics.draw_rect(
        x=250, y=50, width=50, height=50)
    rectangle_3.mousedown(handler=on_rectangle_3_mouse_down)
    rectangle_3.unbind_mousedown_all()

    ap.save_overall_html(dest_dir_path=_DEST_DIR_PATH)


def on_rectangle_1_mouse_down(
        e: ap.MouseEvent, options: Dict[str, Any]) -> None:
    """
    Test handler that called when rectangle 1 is mouse downed.

    Parameters
    ----------
    e : MouseEvent
        Event object.
    options : dict
        Optional arguments dictionary.
    """
    ap.trace('Rectangle 1 is mouse downed!')
    ap.assert_equal(expected='Hello!', actual=options['msg'])


def on_rectangle_2_mouse_down(
        e: ap.MouseEvent, options: Dict[str, Any]) -> None:
    """
    Test handler that called when rectangle 2 is mouse downed.

    Parameters
    ----------
    e : MouseEvent
        Event object.
    options : dict
        Optional arguments dictionary.
    """
    ap.trace(
        'Rectangle 2 is mouse downed. Probably unbind_mousedown'
        'interface not working correctly.')


def on_rectangle_3_mouse_down(
        e: ap.MouseEvent, options: Dict[str, Any]) -> None:
    """
    Test handler that called when rectangle 3 is mosue downed.

    Parameters
    ----------
    e : MouseEvent
        Event object.
    options : dict
        Optional arguments dictionary.
    """
    ap.trace(
        'Rectangle 3 is mouse downed. Probably unbind_mousedown_all '
        'interface not working correctly.')


if __name__ == '__main__':
    main()
