from random import randint

from retrying import retry

from apysc import Int
from apysc.display.line_dot_setting import LineDotSetting


class TestLineDotSetting:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___init__(self) -> None:
        setting: LineDotSetting = LineDotSetting(dot_size=5)
        assert isinstance(setting._dot_size, Int)
        assert setting._dot_size == 5
