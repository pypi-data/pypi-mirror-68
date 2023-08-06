import numpy as np

from simses.commons.log import Logger
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter


class FieldDataAcDcConverter(AcDcConverter):
    """  Fitted Efficiency Curve using field data: Master Thesis by Felix Müller"""
    # Fit for Discharging
    __P0_to_ac = 0.005512
    __K_to_ac = 0.018773

    # Fit for Charging
    __P0_to_dc = 0.007702
    __K_to_dc = 0.017291

    __VOLUMETRIC_POWER_DENSITY = 0.327 * 1e6  # W / m3
    # Calculated Value: 1000000 W / (1.605m * 2.065m * 0.935m)

    def __init__(self, max_power: float):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        if power >= 0:
            return 0
        else:
            return power / self.__get_efficiency_to_ac(power)

    def to_dc(self, power: float, voltage: float) -> float:
        if power <= 0:
            return 0
        else:
            return power * self.__get_efficiency_to_dc(power)

    def __get_efficiency_to_ac(self, power: float) -> float:
        power_factor = abs(power) / self._MAX_POWER
        if power_factor < 0.0 or power_factor > 1.0:
            raise Exception('Power factor is not possible: ' + str(power_factor))
        return power_factor / (power_factor + self.__P0_to_ac + self.__K_to_ac * power_factor ** 2)

    def __get_efficiency_to_dc(self, power: float) -> float:
        power_factor = abs(power) / self._MAX_POWER
        if power_factor < 0.0 or power_factor > 1.0:
            raise Exception('Power factor is not possible: ' + str(power_factor))
        return power_factor / (power_factor + self.__P0_to_dc + self.__K_to_dc * power_factor ** 2)

    def to_dc_reverse(self, power_dc: float) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = - power_dc / (1 - power_dc * self.__K_to_dc / self._MAX_POWER)
            q = - self.__P0_to_dc * power_dc / (1 / self._MAX_POWER - abs(power_dc) * self.__K_to_dc / self._MAX_POWER ** 2)
            self.__log.debug('P_DC: ' + str(power_dc))
            power_ac = max(0.0, -p / 2 + np.sqrt((p / 2) ** 2 - q))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    def to_ac_reverse(self, power_dc) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = self._MAX_POWER / self.__K_to_ac
            q = (self.__P0_to_ac * self._MAX_POWER ** 2 - abs(power_dc) * self._MAX_POWER) / self.__K_to_ac
            self.__log.debug('P_DC: ' + str(power_dc))
            power_ac = min(0.0, -(-p / 2 + np.sqrt((p / 2) ** 2 - q)))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return FieldDataAcDcConverter(max_power)

    def close(self) -> None:
        self.__log.close()
