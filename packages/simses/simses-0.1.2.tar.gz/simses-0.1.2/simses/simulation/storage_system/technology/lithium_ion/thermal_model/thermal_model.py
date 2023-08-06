from abc import ABC, abstractmethod

from simses.commons.state.technology.lithium_ion_state import LithiumIonState


class ThermalModel(ABC):

    def __init__(self):
        super().__init__()

    def update(self, time: float, battery_state: LithiumIonState) -> None:
        """Updating temperature of lithium_ion state"""
        self.calculate_temperature(time, battery_state)
        battery_state.temperature = self.get_temperature()
        battery_state.convection_heat = self.get_convection_heat()

    @abstractmethod
    def calculate_temperature(self, time: float, battery_state: LithiumIonState) -> None:
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        pass

    @abstractmethod
    def set_temperature(self, new_temperature: float) -> float:
        pass

    @abstractmethod
    def get_convection_heat(self) -> float:
        pass

    def close(self) -> None:
        """Closing all resources in thermal model"""
        pass
