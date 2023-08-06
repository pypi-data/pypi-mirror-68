from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.hvac import \
    HeatingVentilationAirConditioning


class NoHeatingVentilationAirConditioning(HeatingVentilationAirConditioning):

    def __init__(self):
        super().__init__()

    def run_air_conditioning(self, thermal_power) -> float:
        pass

    def get_electric_power(self) -> float:
        return 0

    def get_set_point_temperature(self) -> float:
        return 298.15

    def get_thermal_power(self) -> float:
        return 0
