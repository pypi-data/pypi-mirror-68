from abc import ABC, abstractmethod

from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary


class HeatingVentilationAirConditioning(Auxiliary, ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run_air_conditioning(self, thermal_power_required: float) -> None:
        pass

    @abstractmethod
    def get_electric_power(self) -> float:
        pass

    @abstractmethod
    def get_thermal_power(self) -> float:
        pass

    @abstractmethod
    def get_set_point_temperature(self) -> float:
        pass

    def ac_operation_losses(self) -> float:
        return self.get_electric_power()


