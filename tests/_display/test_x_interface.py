from random import randint

from retrying import retry

from apysc import Int
from apysc._display.x_interface import XInterface
from apysc._expression import expression_file_util
from apysc._type import value_util


class TestXInterface:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test_x(self) -> None:
        x_interface = XInterface()
        x_interface.variable_name = 'test_x_interface'
        x_interface.x = Int(100)
        assert x_interface.x == 100

        x: Int = x_interface.x
        assert x == x_interface._x
        assert x.variable_name != x_interface._x.variable_name

        x_interface.x = 200  # type: ignore
        assert x_interface.x == 200

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__append_x_update_expression(self) -> None:
        x_interface = XInterface()
        x_interface.variable_name = 'test_x_interface'
        expression_file_util.remove_expression_file()
        x_interface.x = Int(200)
        expression: str = expression_file_util.get_current_expression()
        value_str: str = value_util.get_value_str_for_expression(
            value=x_interface._x)
        expected: str = f'test_x_interface.x({value_str});'
        assert expected in expression

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__initialize_x_if_not_initialized(self) -> None:
        x_interface = XInterface()
        x_interface.variable_name = 'test_x_interface'
        x_interface._initialize_x_if_not_initialized()
        assert x_interface.x == 0

        x_interface.x = Int(100)
        x_interface._initialize_x_if_not_initialized()
        assert x_interface.x == 100

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__make_snapshot(self) -> None:
        x_interface = XInterface()
        x_interface.variable_name = 'test_x_interface'
        x_interface.x = Int(100)
        snapshot_name: str = 'snapshot_1'
        x_interface._run_all_make_snapshot_methods(
            snapshot_name=snapshot_name)
        assert x_interface._x_snapshots[snapshot_name] == 100

        x_interface.x = Int(150)
        x_interface._run_all_make_snapshot_methods(
            snapshot_name=snapshot_name)
        assert x_interface._x_snapshots[snapshot_name] == 100

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__revert(self) -> None:
        x_interface = XInterface()
        x_interface.variable_name = 'test_x_interface'
        x_interface.x = Int(100)
        snapshot_name: str = 'snapshot_1'
        x_interface._run_all_make_snapshot_methods(
            snapshot_name=snapshot_name)
        x_interface.x = Int(150)
        x_interface._run_all_revert_methods(
            snapshot_name=snapshot_name)
        assert x_interface.x == 100

        x_interface.x = Int(150)
        x_interface._run_all_revert_methods(
            snapshot_name=snapshot_name)
        assert x_interface.x == 150
