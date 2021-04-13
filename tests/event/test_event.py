from random import randint

from retrying import retry

from apysc import Event
from apysc import Int
from apysc.expression import expression_file_util
from apysc.expression import var_names
from tests import testing_helper


class TestEvent:

    @retry(stop_max_attempt_number=10, wait_fixed=randint(100, 1000))
    def test___init__(self) -> None:
        int_1: Int = Int(10)
        event: Event = Event(this=int_1)
        testing_helper.assert_attrs(
            expected_attrs={
                '_this': int_1,
            },
            any_obj=event)
        assert event.variable_name.startswith(
            f'{var_names.EVENT}_'
        )

    @retry(stop_max_attempt_number=10, wait_fixed=randint(100, 1000))
    def test_stop_propagation(self) -> None:
        expression_file_util.remove_expression_file()
        int_1: Int = Int(10)
        e: Event = Event(this=int_1)
        e.stop_propagation()
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'{e.variable_name}.stopPropagation();'
        )
        assert expected in expression

    @retry(stop_max_attempt_number=10, wait_fixed=randint(100, 1000))
    def test_prevent_default(self) -> None:
        expression_file_util.remove_expression_file()
        int_1: Int = Int(10)
        e: Event = Event(this=int_1)
        e.prevent_default()
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'{e.variable_name}.preventDefault();'
        )
        assert expected in expression
