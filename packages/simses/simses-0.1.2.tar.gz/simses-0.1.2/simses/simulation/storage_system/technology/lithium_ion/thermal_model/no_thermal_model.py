from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.thermal_model import ThermalModel


class NoThermalModel(ThermalModel):
    """This model functions at the Storage Technology Level.
      This model treats the entire Storage Technology as 1 lump.
      Current version sets temperature of Storage Technology to 298.15 K and treats it as constant"""

    def __init__(self):
        super().__init__()
        self.__temperature = 298.15 # K

    def calculate_temperature(self, time, battery_state: LithiumIonState) -> None:
        self.__temperature = battery_state.temperature

    def get_temperature(self) -> float:
        return self.__temperature

    def get_convection_heat(self) -> float:
        return 0

    def set_temperature(self, new_temperature: float):
        self.__temperature = new_temperature