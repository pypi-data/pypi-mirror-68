from abc import abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage


class Pipeline(HydrogenStorage):

    def __init__(self):
        super().__init__()

    def update(self, time: float, state: HydrogenState) -> None:
        """Updating sum of injected hydrogen at a given pressure"""
        self.calculate_inijected_hydrogen(time, state.time, state.hydrogen_production)
        state.total_hydrogen_production += self.get_injected_hydrogen()  # kg

    @abstractmethod
    def calculate_inijected_hydrogen(self, time, state_time, hydrogen_production) -> None:
        pass

    @abstractmethod
    def get_injected_hydrogen(self) -> float:
        pass

    @abstractmethod
    def get_capacity(self) -> float:
        pass

    @abstractmethod
    def calculate_soc(self, time, state: HydrogenState) -> None:
        pass

    @abstractmethod
    def get_soc(self) -> float:
        pass

    @abstractmethod
    def get_tank_pressure(self) -> float:
        pass





