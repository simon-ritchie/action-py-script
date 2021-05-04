from random import randint

from retrying import retry

from apysc import Point2D, Int
from tests.testing_helper import assert_attrs


class TestPoint2D:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___init__(self) -> None:
        point: Point2D = Point2D(x=10, y=20)
        assert_attrs(
            expected_attrs={
                '_x': 10,
                '_y': 20,
            },
            any_obj=point)

        x: Int = Int(10)
        y: Int = Int(20)
        point = Point2D(x=x, y=y)
        assert_attrs(
            expected_attrs={
                '_x': x,
                '_y': y,
            },
            any_obj=point)
