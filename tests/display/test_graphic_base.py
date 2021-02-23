from random import randint

from retrying import retry

from apyscript.display.graphic_base import GraphicBase
from apyscript.display.sprite import Sprite
from apyscript.display.stage import Stage
from tests import testing_helper


class TestGraphicBase:

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test___init__(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        graphic_base: GraphicBase = GraphicBase(
            parent=sprite.graphics, x=100, y=200,
            variable_name='test_graphic')
        testing_helper.assert_attrs(
            expected_attrs={
                'parent_graphics': sprite.graphics,
                '_x': 100,
                '_y': 200,
            },
            any_obj=graphic_base)

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test_x(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        graphic_base: GraphicBase = GraphicBase(
            parent=sprite.graphics, x=100, y=200,
            variable_name='test_graphic')
        graphic_base.x = 300
        assert graphic_base.x == 300

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test_y(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        graphic_base: GraphicBase = GraphicBase(
            parent=sprite.graphics, x=100, y=200,
            variable_name='test_graphic')
        graphic_base.y = 400
        assert graphic_base.y == 400

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test_variable_name(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        graphic_base: GraphicBase = GraphicBase(
            parent=sprite.graphics, x=100, y=200,
            variable_name='test_graphic_1')
        assert graphic_base.variable_name == 'test_graphic_1'
        graphic_base.variable_name = 'test_graphic_2'
        assert graphic_base.variable_name == 'test_graphic_2'
