from random import randint

import pytest
from retrying import retry

from apyscript.display.parent_interface import ParentInterface
from apyscript.display.sprite import Sprite
from apyscript.display.stage import Stage
from tests import testing_helper


class TestParentInterface:

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test_parent(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        stage.add_child(child=sprite)
        assert sprite.parent == stage

        with pytest.raises(ValueError):  # type: ignore
            sprite.parent = 100

    @retry(stop_max_attempt_number=5, wait_fixed=randint(100, 1000))
    def test_remove_from_parent(self) -> None:
        stage: Stage = Stage()
        sprite: Sprite = Sprite(stage=stage)
        stage.add_child(child=sprite)
        sprite.remove_from_parent()
        assert len(stage._childs) == 0

        testing_helper.assert_raises(
            expected_error_class=ValueError,
            func_or_method=sprite.remove_from_parent,
        )
