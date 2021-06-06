# Common mouse event interfaces

This page will explain the common mouse event interfaces, like `this`.

## Basic binding usage

Each mouse event binding interface accepts `handler` and `options` arguments. The `handler` argument is a callable called when the target event is dispatched.

The `options` argument is an optional parameter dictionary to be passed to the handler. This argument can be skipped.

For instance, the `click` event can be set as follows:

```py
# runnable
from typing import Any, Dict

from apysc import Sprite
from apysc import Stage
from apysc import Rectangle
from apysc import MouseEvent
from apysc import String
from apysc import save_expressions_overall_html

stage: Stage = Stage(
    background_color='#333',
    stage_width=150,
    stage_height=150,
    stage_elem_id='stage')

sprite: Sprite = Sprite(stage=stage)
sprite.graphics.begin_fill(color='#0af')


def on_rectangle_click(e: MouseEvent, options: Dict[str, Any]) -> None:
    """
    The handler will be called when the rectangle is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments.
    """
    # Change the clicked rectangle color to the passed color.
    rectangle: Rectangle = e.this
    color: String = String(options['color'])
    rectangle.fill_color = color


rectangle: Rectangle = sprite.graphics.draw_rect(
    x=50, y=50, width=50, height=50)
rectangle.click(
    handler=on_rectangle_click,
    options={'color': '#f0a'})

save_expressions_overall_html(
    dest_dir_path='mouse_event_common_basic_binding_usage/')
```

If you click the following rectangle, the rectangle color will be changed to the specified options color.

<iframe src="static/mouse_event_common_basic_binding_usage/index.html" width="150" height="150"></iframe>

There are the `click`, `mousedown`, `mouseup`, `mouseover`, `mouseout`, and `mousemove` mouse event binding interfaces that the `DisplayObject` instance has.

## Basic unbinding usage

Each `DisplayObject` instance has the `unbind_<event_name>` interfaces, for example, `unbind_click` or `unbind_mousedown` or something else.

These interfaces can unbind the single handler setting (remove binding setting).

For example, the following code will unbind the click event, so the handler function will not be called.

```py
# runnable
from typing import Any, Dict

from apysc import Sprite
from apysc import Stage
from apysc import Rectangle
from apysc import MouseEvent
from apysc import String
from apysc import save_expressions_overall_html

stage: Stage = Stage(
    background_color='#333',
    stage_width=150,
    stage_height=150,
    stage_elem_id='stage')

sprite: Sprite = Sprite(stage=stage)
sprite.graphics.begin_fill(color='#0af')


def on_rectangle_click(e: MouseEvent, options: Dict[str, Any]) -> None:
    """
    The handler will be called when the rectangle is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments.
    """
    # Change the clicked rectangle color to the passed color.
    rectangle: Rectangle = e.this
    color: String = String(options['color'])
    rectangle.fill_color = color


rectangle: Rectangle = sprite.graphics.draw_rect(
    x=50, y=50, width=50, height=50)
rectangle.click(
    handler=on_rectangle_click,
    options={'color': '#f0a'})

rectangle.unbind_click(handler=on_rectangle_click)

save_expressions_overall_html(
    dest_dir_path='mouse_event_common_basic_unbinding_usage/')
```

When you click the following rectangle, nothing will happen.

<iframe src="static/mouse_event_common_basic_unbinding_usage/index.html" width="150" height="150"></iframe>

## Unbind all event handlers

Sometimes, it is useful to unbind specific all the event at once. Each event interface has the `unbind_<event_name>_all` method (e.g., `unbind_click_all`), and it can unbind all event handlers from that instance.

The following code is calling the `unbind_click_all` method, so all hander settings are removed.

```py
# runnable
from typing import Any, Dict

from apysc import Sprite
from apysc import Stage
from apysc import Rectangle
from apysc import MouseEvent
from apysc import String
from apysc import save_expressions_overall_html

stage: Stage = Stage(
    background_color='#333',
    stage_width=150,
    stage_height=150,
    stage_elem_id='stage')

sprite: Sprite = Sprite(stage=stage)
sprite.graphics.begin_fill(color='#0af')


def change_color_on_rectangle_click(
        e: MouseEvent, options: Dict[str, Any]) -> None:
    """
    The handler will change the rectangle color and be called
    when the rectangle is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments.
    """
    rectangle: Rectangle = e.this
    color: String = String(options['color'])
    rectangle.fill_color = color


def change_x_on_rectangle_click(
        e: MouseEvent, options: Dict[str, Any]) -> None:
    """
    The handler will change the rectangle x-coordinate and be called
    when the rectangle is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments.
    """
    rectangle: Rectangle = e.this
    rectangle.x += 50


rectangle: Rectangle = sprite.graphics.draw_rect(
    x=50, y=50, width=50, height=50)
rectangle.click(
    handler=change_color_on_rectangle_click,
    options={'color': '#f0a'})
rectangle.click(handler=change_x_on_rectangle_click)

rectangle.unbind_click_all()

save_expressions_overall_html(
    dest_dir_path='mouse_event_common_unbind_all_event_handlers/')
```

If you click the following rectangle, also nothing will happen (no color change and no x-coordinate change).

<iframe src="static/mouse_event_common_unbind_all_event_handlers/index.html" width="150" height="150"></iframe>