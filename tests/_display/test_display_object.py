from random import randint

from retrying import retry

from apysc import Stage
from apysc._display.display_object import DisplayObject
from tests import testing_helper


class TestDisplayObject:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___init__(self) -> None:
        stage: Stage = Stage()
        display_object: DisplayObject = DisplayObject(
            stage=stage, variable_name='test_display_object')
        testing_helper.assert_attrs(
            expected_attrs={
                'stage': stage,
                '_stage_cls': Stage,
            },
            any_obj=display_object)

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test_variable_name(self) -> None:
        stage: Stage = Stage()
        display_object: DisplayObject = DisplayObject(
            stage=stage, variable_name='test_display_object_1')
        display_object.variable_name = 'test_display_object_2'
        assert display_object.variable_name == 'test_display_object_2'
