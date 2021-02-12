from random import randint

from retrying import retry

from apyscript.display import rectangle
from apyscript.display.rectangle import Rectangle
from apyscript.display.sprite import Sprite
from apyscript.display.stage import Stage
from apyscript.display.stage import get_stage_variable_name
from apyscript.expression import expression_file_util
from apyscript.expression import expression_scope
from tests import testing_helper


class TestRectangle:

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test___init__(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        rectangle: Rectangle = Rectangle(
            parent=sprite.graphics,
            x=100, y=200, width=300, height=400)
        testing_helper.assert_attrs(
            expected_attrs={
                'parent': sprite.graphics,
                '_x': 100,
                '_y': 200,
                'width': 300,
                'height': 400,
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

    sprite.graphics.begin_fill(color='#333')
    rect_attrs_expression = rectangle._make_rect_attrs_expression(
        rectangle=rectangle_)
    expected = (
        '\n  .attr({'
        '\n    fill: "#333333",'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  })'
    )
    assert rect_attrs_expression == expected


@retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
def test_append_draw_rect_expression() -> None:
    stage: Stage = Stage()
    expression_scope.update_current_scope(scope_name='test_graphics')
    expression_file_util.remove_current_scope_expression_file()
    sprite: Sprite = Sprite(stage=stage)
    sprite.graphics.begin_fill(color='#333')
    sprite.graphics.draw_rect(x=100, y=200, width=300, height=400)
    sprite_name: str = sprite.variable_name
    rect_name: str = sprite.graphics._graphics[0].variable_name
    stage_variable_name: str = get_stage_variable_name()
    expression: str = expression_file_util.get_current_scope_expression()
    expected: str = (
        f'\nvar {rect_name} = {stage_variable_name}'
        '\n  .rect(300, 400)'
        '\n  .attr({'
        '\n    fill: "#333333",'
        '\n    x: 100,'
        '\n    y: 200,'
        '\n  });'
        f'\n{sprite_name}.add({rect_name});'
    )
    assert expected in expression
    expression_file_util.remove_current_scope_expression_file()