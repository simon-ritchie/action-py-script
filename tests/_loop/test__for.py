from random import randint

from retrying import retry

from apysc import Array
from apysc import Dictionary
from apysc import For
from apysc import Int
from apysc import String
from apysc._expression import expression_file_util
from apysc._expression import indent_num
from apysc._expression import last_scope
from apysc._expression.indent_num import Indent
from apysc._expression.last_scope import LastScope
from tests import testing_helper


class TestFor:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___init__(self) -> None:
        arr: Array = Array([1, 2, 3])
        for_: For = For(
            arr_or_dict=arr, locals_={'value_1': 1},
            globals_={'value_2': 2})
        testing_helper.assert_attrs(
            expected_attrs={
                '_arr_or_dict': arr,
                '_locals': {'value_1': 1},
                '_globals': {'value_2': 2},
            },
            any_obj=for_)
        assert isinstance(for_._indent, Indent)

        for_ = For(arr)
        testing_helper.assert_attrs(
            expected_attrs={
                '_locals': {},
                '_globals': {},
            },
            any_obj=for_)

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__append_arr_enter_expression(self) -> None:
        expression_file_util.remove_expression_file()
        arr: Array = Array([1, 2, 3])
        with For(arr, locals(), globals()) as i:
            pass
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'var length = {arr.variable_name}.length;'
        )
        assert expected in expression
        i_name: str = i.variable_name
        expected = (
            f'for ({i_name} = 0; {i_name} < length; {i_name}++) {{'
        )
        assert expected in expression

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___enter__(self) -> None:
        indent_num.reset()
        arr: Array = Array([1, 2, 3])
        with For(arr, locals(), globals()) as i:
            current_indent_num: int = indent_num.get_current_indent_num()
            assert current_indent_num == 1
        assert isinstance(i, Int)

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test___exit__(self) -> None:
        indent_num.reset()
        int_1: Int = Int(10)
        arr: Array = Array([1, 2, 3])
        with For(arr, locals(), globals()) as i:
            int_1.value = 20
        assert int_1.value == 10
        current_indent_num: int = indent_num.get_current_indent_num()
        assert current_indent_num == 0
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'  {int_1.variable_name} = 20;'
            '\n}'
        )
        assert expected in expression
        assert last_scope.get_last_scope() == LastScope.FOR

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__append_dict_enter_expression(self) -> None:
        expression_file_util.remove_expression_file()
        dict_1: Dictionary = Dictionary({'a': 10})
        with For[String](dict_1) as key:
            pass
        expression: str = expression_file_util.get_current_expression()
        expected: str = (
            f'for (var {key.variable_name} in {dict_1.variable_name}) {{'
        )
        assert expected in expression

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__validate_arr_or_dict_val_type(self) -> None:
        For(Array([0]))
        For(Dictionary({'a': 10}))
        testing_helper.assert_raises(
            expected_error_class=TypeError,
            func_or_method=For,
            kwargs={'arr_or_dict': 'Hello!'},
            match='Specified value type is neither Array nor Dictionary: ')
