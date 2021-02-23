from apyscript.display.sprite import Sprite
from random import randint

from retrying import retry

from apyscript.display.stage import Stage
from apyscript.validation import parent_validation
from tests import testing_helper


@retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
def test_validate_parent_instance() -> None:
    parent_validation.validate_parent_instance(parent=None)
    stage: Stage = Stage()
    parent_validation.validate_parent_instance(parent=stage)
    testing_helper.assert_raises(
        expected_error_class=ValueError,
        func_or_method=parent_validation.validate_parent_instance,
        kwargs={
            'parent': 100,
        })


@retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
def test_validate_parent_contains_chils() -> None:
    stage: Stage = Stage()
    sprite_1: Sprite = Sprite(stage=stage)
    stage.add_child(child=sprite_1)
    parent_validation.validate_parent_contains_child(
        parent=stage, child=sprite_1)

    sprite_2: Sprite = Sprite(stage=stage)
    testing_helper.assert_raises(
        expected_error_class=ValueError,
        func_or_method=parent_validation.validate_parent_contains_child,
        kwargs={
            'parent': stage,
            'child': sprite_2,
        })

    parent_validation.validate_parent_contains_child(
        parent=None, child=sprite_2)
