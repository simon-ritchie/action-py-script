"""Definition of the FPS enum.
"""

from enum import Enum
from typing import Union


class FPSDefinition:

    _fps: int
    _milisecond_interval: Union[int, float]

    def __init__(
            self, fps: int,
            milisecond_intervals: Union[int, float]) -> None:
        """
        FPS definition class.

        Parameters
        ----------
        fps : int
            FPS value, such as 30, 60.
        milisecond_intervals : int or float
            FPS value in milisecond intervals, such as 33, 16.
        """
        self._fps = fps
        self._milisecond_interval = milisecond_intervals


class FPS(Enum):

    FPS_10 = FPSDefinition(fps=10, milisecond_intervals=100)
    FPS_15 = FPSDefinition(fps=15, milisecond_intervals=66.6666667)
    FPS_20 = FPSDefinition(fps=20, milisecond_intervals=50)
    FPS_25 = FPSDefinition(fps=25, milisecond_intervals=40)
    FPS_30 = FPSDefinition(fps=30, milisecond_intervals=33.3333333)
    FPS_45 = FPSDefinition(fps=45, milisecond_intervals=22.2222222)
    FPS_60 = FPSDefinition(fps=60, milisecond_intervals=16.6666667)
