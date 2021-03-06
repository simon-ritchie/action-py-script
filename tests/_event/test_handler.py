from random import randint
from typing import Any
from typing import Dict

from retrying import retry

from apysc import Event
from apysc import Int
from apysc import MouseEventType
from apysc._event import handler
from apysc._event.handler import HandlerData
from apysc._expression import expression_file_util
from apysc._type.variable_name_interface import VariableNameInterface
from tests import testing_helper


class _TestClass1(VariableNameInterface):

    def __init__(self) -> None:
        """
        Test class for handler's tests.
        """
        self.variable_name = 'test_class_1'

    def on_click_1(self, e: Event, options: Dict[str, Any]) -> None:
        """
        Test handler.

        Parameters
        ----------
        e : Event
            Created event instance.
        options : dict
            Optional arguments dictionary.
        """

    def on_click_2(self, e: Event, options: Dict[str, Any]) -> None:
        """
        Test handler.

        Parameters
        ----------
        e : Event
            Created event instance.
        options : dict
            Optional arguments dictionary.
        """
        int_1: Int = options['int_1']
        int_1.value = 20


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_get_handler_name() -> None:
    test_instance: _TestClass1 = _TestClass1()
    handler_name: str = handler.get_handler_name(
        handler=test_instance.on_click_1,
        instance=test_instance)
    assert 'tests__event_test_handler' in handler_name
    assert '_TestClass1_' in handler_name
    assert 'on_click_1_' in handler_name
    assert handler_name.endswith(f'_{test_instance.variable_name}')


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_append_handler_expression() -> None:
    expression_file_util.remove_expression_file()
    test_instance: _TestClass1 = _TestClass1()
    int_1: Int = Int(10)
    handler_data: HandlerData = {
        'handler': test_instance.on_click_2,
        'options': {'int_1': int_1},
    }
    handler_name: str = handler.get_handler_name(
        handler=handler_data['handler'], instance=test_instance)
    e: Event = Event(this=test_instance)
    handler.append_handler_expression(
        handler_data=handler_data, handler_name=handler_name,
        e=e)
    expression: str = \
        expression_file_util.get_current_event_handler_scope_expression()
    expected: str = (
        f'function {handler_name}({e.variable_name}) {{'
        f'\n  {int_1.variable_name} = 20;'
        '\n}'
    )
    assert expected in expression
    assert int_1 == 10

    testing_helper.assert_raises(
        expected_error_class=ValueError,
        func_or_method=handler.append_handler_expression,
        kwargs={
            'handler_data': handler_data,
            'handler_name': handler_name,
            'e': 100,
        })


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_append_unbinding_expression() -> None:
    expression_file_util.remove_expression_file()
    int_1: Int = Int(10)
    handler.append_unbinding_expression(
        this=int_1, handler_name='on_click_1',
        mouse_event_type=MouseEventType.CLICK)
    expression: str = expression_file_util.get_current_expression()
    expected: str = (
        f'{int_1.variable_name}.off("{MouseEventType.CLICK.value}", '
        'on_click_1);'
    )
    assert expected in expression


@retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
def test_append_unbinding_all_expression() -> None:
    expression_file_util.remove_expression_file()
    int_1: Int = Int(10)
    handler.append_unbinding_all_expression(
        this=int_1, mouse_event_type=MouseEventType.CLICK)
    expression: str = expression_file_util.get_current_expression()
    expected: str = (
        f'{int_1.variable_name}.off("{MouseEventType.CLICK.value}");'
    )
    assert expected in expression
