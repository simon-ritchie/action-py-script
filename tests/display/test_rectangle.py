from random import randint

from retrying import retry

from apyscript.display import rectangle
from apyscript.display.rectangle import Rectangle
from apyscript.display.sprite import Sprite
from apyscript.display.stage import Stage
from apyscript.display.stage import get_stage_variable_name
from apyscript.expression import expression_file_util
from tests import testing_helper


class TestRectangle:

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test___init__(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        rectangle: Rectangle = Rectangle(
            parent=sprite.graphics,
            x=100, y=200, width=300, height=400, fill_color='#333',
            fill_alpha=0.75, line_color='#aaa', line_thickness=3,
            line_alpha=0.3)
        testing_helper.assert_attrs(
            expected_attrs={
                'parent_graphics': sprite.graphics,
                '_x': 100,
                '_y': 200,
                'width': 300,
                'height': 400,
                '_fill_color': '#333333',
                '_fill_alpha': 0.75,
                '_line_color': '#aaaaaa',
                '_line_thickness': 3,
                '_line_alpha': 0.3,
            },
            any_obj=rectangle)


@retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
def test__make_rect_attrs_expression() -> None:
    stage: Stage = Stage()
    sprite: Sprite = Sprite(stage=stage)
    rectangle_: Rectangle = Rectangle(
        parent=sprite.graphics,
        x=100, y=200,
        width=150, height=50)
    rect_attrs_expression: str = rectangle._make_rect_attrs_expression(
        rectangle=rectangle_)
    expected: str = (
        '\n  .attr({'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  })'
    )
    assert rect_attrs_expression == expected

    sprite.graphics.begin_fill(color='#333', alpha=0.5)
    rect_attrs_expression = rectangle._make_rect_attrs_expression(
        rectangle=rectangle_)
    expected = (
        '\n  .attr({'
        '\n    fill: "#333333",'
        '\n    "fill-opacity": 0.5,'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  })'
    )
    assert rect_attrs_expression == expected

    sprite = Sprite(stage=stage)
    sprite.graphics.line_style(color='#666', thickness=2, alpha=0.3)
    rectangle_ = Rectangle(
        parent=sprite.graphics,
        x=100, y=200, width=150, height=50)
    rect_attrs_expression = rectangle._make_rect_attrs_expression(
        rectangle=rectangle_)
    expected = (
        '\n  .attr({'
        '\n    stroke: "#666666",'
        '\n    "stroke-width": 2,'
        '\n    "stroke-opacity": 0.3,'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  })'
    )
    assert rect_attrs_expression == expected


@retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
def test_append_draw_rect_expression() -> None:
    stage: Stage = Stage()
    sprite: Sprite = Sprite(stage=stage)
    sprite.graphics.begin_fill(color='#333', alpha=0.5)
    sprite.graphics.draw_rect(x=100, y=200, width=300, height=400)
    graphics_name: str = sprite.graphics.variable_name
    rect_name: str = sprite.graphics._childs[0].variable_name
    stage_variable_name: str = get_stage_variable_name()
    expression: str = expression_file_util.get_current_expression()
    expected: str = (
        f'\nvar {rect_name} = {stage_variable_name}'
        '\n  .rect(300, 400)'
        '\n  .attr({'
        '\n    fill: "#333333",'
        '\n    "fill-opacity": 0.5,'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  });'
        f'\n{graphics_name}.add({rect_name});'
    )
    assert expected in expression
    expression_file_util.remove_expression_file()
