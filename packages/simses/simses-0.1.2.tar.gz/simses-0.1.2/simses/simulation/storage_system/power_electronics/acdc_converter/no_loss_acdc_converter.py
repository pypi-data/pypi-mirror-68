from simses.simulation.storage_system.power_electronics.acdc_converter.acdc_converter import AcDcConverter
from simses.commons.log import Logger

class NoLossAcDcConverter(AcDcConverter):

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)

    def __init__(self, max_power: float):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        if power >= 0:
            return 0
        else:
            return power

    def to_dc(self, power: float, voltage: float) -> float:
        if power <= 0:
            return 0
        else:
            return power

    def to_dc_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            return dc_power

    def to_ac_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        return dc_power

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return NoLossAcDcConverter(max_power)

    def close(self) -> None:
        pass
