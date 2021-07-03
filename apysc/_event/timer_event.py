"""Class implementation for the timer event.
"""

from apysc._event.event import Event
from apysc._time.timer import Timer


class TimerEvent(Event):

    _this: Timer

    def __init__(self, this: Timer) -> None:
        """
        Timer event class.

        Parameters
        ----------
        timer : Timer
            Target timer instance.
        """
        from apysc._expression import var_names
        super(TimerEvent, self).__init__(
            this=this, type_name=var_names.TIMER_EVENT)
