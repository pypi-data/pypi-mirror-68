from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.hvac import \
    HeatingVentilationAirConditioning


class FixCOPHeatingVentilationAirConditioning(HeatingVentilationAirConditioning, Auxiliary):

    def __init__(self, max_thermal_power: float, set_point_temperature: float):
        super().__init__()
        self.__max_thermal_power: float = max_thermal_power
        self.__cop: float = 3
        self.__set_point_temperature = set_point_temperature
        self.__electric_power: float = 0
        self.__thermal_power: float = 0

    def run_air_conditioning(self, thermal_power_required: float) -> None:
        if abs(thermal_power_required) > self.__max_thermal_power:
            self.__thermal_power = self.__max_thermal_power
        else:
            self.__thermal_power = thermal_power_required
        self.__electric_power = abs(self.__thermal_power / self.__cop)

    def get_thermal_power(self) -> float:
        return self.__thermal_power

    def get_electric_power(self) -> float:
        return self.__electric_power

    def get_set_point_temperature(self) -> float:
        return self.__set_point_temperature
