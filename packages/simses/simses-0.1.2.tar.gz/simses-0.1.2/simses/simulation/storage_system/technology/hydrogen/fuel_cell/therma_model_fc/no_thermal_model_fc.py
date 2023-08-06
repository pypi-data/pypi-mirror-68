from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.no_thermal_controller_fc import \
    NoThermalControllerFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.thermal_model_fc import \
    ThermalModelFc



class NoThermalModelFc(ThermalModelFc):
    """This model functions at the Storage Technology Level.
      This model treats the entire Storage Technology as 1 lump.
      Current version sets temperature of Storage Technology to 298.15 K and treats it as constant"""

    def __init__(self):
        super().__init__()
        self.__temperature = 298.15 # K
        self.__pump_power = 0  # W
        self.__water_flow_stack = 0  # mol/s
        self.__power_water_heating = 0  # W
        self.__water_temperature_in = 0  # K
        self.__thermal_controller = NoThermalControllerFc()

    def calculate(self, time, hydrogen_state: HydrogenState) -> None:
        self.__temperature = hydrogen_state.temperature
        self.__water_flow_stack = self.__thermal_controller.calculate_water_flow(self.__temperature, 0, 0)
        self.__water_temperature_in = self.__thermal_controller.calculate_water_temperature_in(self.__temperature)

    def get_temperature(self) -> float:
        return self.__temperature

    def get_pump_power(self) -> float:
        return self.__pump_power

    def calculate_pump_power(self, water_flow_stack: float) -> None:
        self.__pump_power = self.__pump_power

    def get_water_flow_stack(self) -> float:
        pass

    def get_power_water_heating(self) -> float:
        pass

    def get_convection_heat(self) -> float:
        return 0

    def set_temperature(self, new_temperature: float):
        self.__temperature = new_temperature