from random import randint

from retrying import retry

from apysc import Int
from apysc._display.ellipse_width_interface import EllipseWidthInterface
from apysc._expression import expression_file_util


class TestEllipseWidthInterface:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__initialize_ellipse_width_if_not_initialized(self) -> None:
        interface: EllipseWidthInterface = EllipseWidthInterface()
        interface._initialize_ellipse_width_if_not_initialized()
        assert interface._ellipse_width == 0

        interface._ellipse_width.value = 10
        interface._initialize_ellipse_width_if_not_initialized()
        assert interface._ellipse_width == 10

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test_ellipse_width(self) -> None:
        interface: EllipseWidthInterface = EllipseWidthInterface()
        interface.variable_name = 'test_ellipse_width_interface'
        assert interface.ellipse_width == 0

        interface.ellipse_width = Int(10)
        assert interface.ellipse_width == 10

        interface.ellipse_width = 20  # type: ignore
        assert interface.ellipse_width == 20

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__append_ellipse_width_update_expression(self) -> None:
        expression_file_util.remove_expression_file()
        interface: EllipseWidthInterface = EllipseWidthInterface()
        interface.variable_name = 'test_ellipse_width_interface'
        ellipse_width: Int = Int(10)
        interface.ellipse_width = ellipse_width
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'{interface.variable_name}.radius({ellipse_width.variable_name}'
            ', 0);'
        )
        assert expected in expression

        expression_file_util.remove_expression_file()
        ellipse_height: Int = Int(20)
        setattr(interface, '_ellipse_height', ellipse_height)
        interface.ellipse_width = ellipse_width
        expression = expression_file_util.get_current_expression()
        expected = (
            f'{interface.variable_name}.radius({ellipse_width.variable_name}'
            f', {ellipse_height.variable_name});'
        )
        assert expected in expression

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__make_snapshot(self) -> None:
        interface: EllipseWidthInterface = EllipseWidthInterface()
        interface.variable_name = 'test_ellipse_width_interface'
        interface.ellipse_width = Int(10)
        snapshot_name: str = interface._get_next_snapshot_name()
        interface._run_all_make_snapshot_methods(snapshot_name=snapshot_name)
        assert interface._ellipse_width_snapshots[snapshot_name] == 10

        interface.ellipse_width = Int(20)
        interface._run_all_make_snapshot_methods(snapshot_name=snapshot_name)
        assert interface._ellipse_width_snapshots[snapshot_name] == 10

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__revert(self) -> None:
        interface: EllipseWidthInterface = EllipseWidthInterface()
        interface.variable_name = 'test_ellipse_width_interface'
        interface.ellipse_width = Int(10)
        snapshot_name: str = interface._get_next_snapshot_name()
        interface._run_all_make_snapshot_methods(snapshot_name=snapshot_name)
        interface.ellipse_width = Int(20)
        interface._run_all_revert_methods(snapshot_name=snapshot_name)
        assert interface.ellipse_width == 10

        interface.ellipse_width = Int(20)
        interface._run_all_revert_methods(snapshot_name=snapshot_name)
        assert interface.ellipse_width == 20
