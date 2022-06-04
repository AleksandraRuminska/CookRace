from Stations.PowerLevels import PowerLevels
from Stations.Station import Station


class Machine(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self._power = PowerLevels.OFF

    def running(self):
        return self._power is not PowerLevels.OFF

    def turn_on(self, intensity):
        self._power = intensity

    def turn_off(self):
        self._power = PowerLevels.OFF

    def tick(self):
        pass
