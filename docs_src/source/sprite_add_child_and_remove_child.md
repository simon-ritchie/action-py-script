# Sprite class add_child and remove_child interfaces

This page will explain the `Sprite` class (or the other container class, like the `Graphics`) `add_child` and `remove_child` method interfaces.

## What interfaces are these?

The `add_child` and `remove_child` will add or remove a `DisplayObject` child instance from a `Sprite` container instance. A removed `DisplayObject` instance will not be displayed.

## Automatic addition of the children

Each `DisplayObject` instance will be added to a parent at the constructor. For example, a `Sprite` instance will be added to a parent stage basically, and `graphics` instances will be added to a parent `Sprite` instance. The `Rectangle` or the other `DisplayObject` instances, like the `Circle`, behaves in the same way (they will be added to a `graphics` container instance automatically).

If you need to adjust a parent, then it will be necessary to call the `add_child` or `remove_child` interfaces manually (for instance, set a `Sprite` parent to the other `Sprite`).

## Basic usage of the remove_child interface

The `remove_child` interface will remove a child from a parent `Sprite` instance. A removed `DisplayObject` instance will not be displayed on a stage.

For example, the following code will call the `remove_child` interface in the click handler, so if you click the rectangle, that one will be removed.

```py
# runnable
from typing import Any
from typing import Dict

import apysc as ap


def on_sprite_click(
        e: ap.MouseEvent[ap.Sprite], options: Dict[str, Any]) -> None:
    """
    The handler would be called when the sprite instance is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments dictionary.
    """
    sprite: ap.Sprite = e.this
    rectangle: ap.Rectangle = options['rectangle']
    sprite.remove_child(child=rectangle)


stage: ap.Stage = ap.Stage(
    background_color='#333',
    stage_width=150,
    stage_height=150,
    stage_elem_id='stage')

sprite: ap.Sprite = ap.Sprite(stage=stage)
sprite.graphics.begin_fill(color='#0af')
rectangle: ap.Rectangle = sprite.graphics.draw_rect(
    x=50, y=50, width=50, height=50)
sprite.click(on_sprite_click, options={'rectangle': rectangle})

ap.save_overall_html(dest_dir_path='sprite_basic_usage_of_remove_child/')
```

<iframe src="static/sprite_basic_usage_of_remove_child/index.html" width="150" height="150"></iframe>

## The basic usage of the add_child interface

The `add_child` interface will add a removed child again or add a child to the other container instance.

The following code example will remove the rectangle from the first `Sprite` container (be positioned to the left) when you click the rectangle, and then add it to the second `Sprite` container (be positioned to the right).

```py
# runnable
from typing import Any
from typing import Dict

import apysc as ap


def on_sprite_click(
        e: ap.MouseEvent[ap.Sprite], options: Dict[str, Any]) -> None:
    """
    The handler would be called when the sprite instance is clicked.

    Parameters
    ----------
    e : MouseEvent
        Event instance.
    options : dict
        Optional arguments dictionary.
    """
    first_sprite: ap.Sprite = e.this
    rectangle: ap.Rectangle = options['rectangle']
    second_sprite: ap.Sprite = options['second_sprite']
    first_sprite.remove_child(child=rectangle)
    second_sprite.add_child(child=rectangle)


stage: ap.Stage = ap.Stage(
    background_color='#333',
    stage_width=250,
    stage_height=150,
    stage_elem_id='stage')

first_sprite: ap.Sprite = ap.Sprite(stage=stage)
first_sprite.graphics.begin_fill(color='#0af')
first_sprite.x = ap.Int(50)
first_sprite.y = ap.Int(50)
rectangle: ap.Rectangle = first_sprite.graphics.draw_rect(
    x=0, y=0, width=50, height=50)

second_sprite: ap.Sprite = ap.Sprite(stage=stage)
second_sprite.x = ap.Int(150)
second_sprite.y = ap.Int(50)

first_sprite.click(
    on_sprite_click,
    options={'rectangle': rectangle, 'second_sprite': second_sprite})

ap.save_overall_html(dest_dir_path='sprite_basic_usage_of_add_child/')
```

<iframe src="static/sprite_basic_usage_of_add_child/index.html" width="250" height="150"></iframe>

## See also

- [DisplayObject class parent interfaces](display_object_parent.md)
- [Sprite class contains interface](sprite_contains.md)
