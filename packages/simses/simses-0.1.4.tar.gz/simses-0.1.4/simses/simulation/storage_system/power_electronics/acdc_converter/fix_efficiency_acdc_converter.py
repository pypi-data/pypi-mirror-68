from simses.commons.log import Logger
from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter


class FixEfficiencyAcDcConverter(AcDcConverter):

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)

    def __init__(self, max_power: float, efficiency: float = 0.95):
        super().__init__(max_power)
        self.__EFFICIENCY = efficiency
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        if power >= 0:
            return 0
        else:
            return power / self.__EFFICIENCY

    def to_dc(self, power: float, voltage: float) -> float:
        if power <= 0:
            return 0
        else:
            return power * self.__EFFICIENCY

    def to_dc_reverse(self, power_dc: float) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            return power_dc / self.__EFFICIENCY

    def to_ac_reverse(self, power_dc: float) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            return power_dc * self.__EFFICIENCY

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return FixEfficiencyAcDcConverter(max_power)

    def close(self) -> None:
        pass
