from random import randint

from retrying import retry

from apysc.display.radius_interface import RadiusInterface
from apysc import Int


class TestRadiusInterface:

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test__initialize_radius_if_not_initialized(self) -> None:
        interface: RadiusInterface = RadiusInterface()
        interface._initialize_radius_if_not_initialized()
        assert interface._radius == 0

        interface._radius = Int(10)
        assert interface._radius == 10

    @retry(stop_max_attempt_number=15, wait_fixed=randint(10, 3000))
    def test_radius(self) -> None:
        interface: RadiusInterface = RadiusInterface()
        interface.variable_name = 'test_radius_interface'
        assert interface.radius == 0

        interface.radius = Int(10)
        assert interface.radius == 10

        interface.radius = 20  # type: ignore
        assert interface.radius == 20