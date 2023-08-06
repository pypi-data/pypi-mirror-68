from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class ZeroDThermalModel(ThermalModel):
    """This model functions at the Storage Technology Level.
    This model treats the entire Storage Technology as 1 lump.
    Current version models natural convection for a single cell, and scales it up to specified series/parallel scale"""

    def __init__(self, cell_type: CellType, system_thermal_model: SystemThermalModel):
        super().__init__()
        self.__system_thermal_model = system_thermal_model
        self.__temperature = system_thermal_model.get_temperature()  # K, Initialize Cell temperature to system air temperature
        self.__convection_heat = 0  # Initialize variable
        self.mass = cell_type.get_mass()  # kg (for entire series / parallel combination)
        self.surface_area = cell_type.get_surface_area()  # m2 (for entire series / parallel combination)
        self.convection_coefficient = cell_type.get_convection_coefficient()  # W/m2K
        self.specific_heat = cell_type.get_specific_heat()  # J/kgK

    def calculate_temperature(self, time: float, battery_state: LithiumIonState) -> None:

        sample_time = time - battery_state.time
        self.__temperature = battery_state.temperature
        temperature_system = self.__system_thermal_model.get_temperature()
        # self.__convection_heat = sample_time * self.convection_coefficient * self.surface_area * (temperature_system - self.__temperature)
        # convection heat is -ve when battery is hotter than system air, and +ve when system air is hotter than the battery.
        delta_t = sample_time * battery_state.power_loss / (self.mass * self.specific_heat)  # K, due to internal heat generation
        self.__temperature = self.__temperature + delta_t  # K, after internal heat generation
        t_i = (self.__system_thermal_model.get_air_mass() * self.__system_thermal_model.get_air_specific_heat() * temperature_system + self.mass * self.specific_heat * self.__temperature) / (
                          self.mass * self.specific_heat + self.__system_thermal_model.get_air_mass() * self.__system_thermal_model.get_air_specific_heat())  # K, the intermediate temperature assumed to have been attained
        max_delta_t = t_i - self.__temperature  # K, with respect to air
        # max_delta_t is the maximum difference in battery temperature that can be brought about with a given mass of
        # air at a given temperature.
        a = self.__temperature + max_delta_t
        self.__convection_heat = self.mass * self.specific_heat * max_delta_t / sample_time  # W
        self.__temperature = self.__temperature + max_delta_t

    def get_temperature(self) -> float:
        return self.__temperature

    def get_convection_heat(self) -> float:
        return self.__convection_heat

    def set_temperature(self, new_temperature):
        self.__temperature = new_temperature
