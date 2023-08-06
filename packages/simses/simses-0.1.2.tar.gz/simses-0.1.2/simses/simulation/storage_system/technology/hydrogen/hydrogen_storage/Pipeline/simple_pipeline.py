import math as m

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.Pipeline.pipeline import Pipeline
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage


class SimplePipeline(Pipeline):

    """calculates total mass of produced and injected hydrogen in kg"""

    def __init__(self, storage_pressure: float):
        super().__init__()
        self.injected_hydrogen = 0  # kg
        self.storage_pressure = storage_pressure

    def calculate_inijected_hydrogen(self, time, state_time, hydrogen_production) -> None:
        delta_t = time - state_time
        self.injected_hydrogen = delta_t * hydrogen_production * 2 * HydrogenStorage.MOLAR_MASS_HYDROGEN # kg

    def calculate_soc(self, time, state: HydrogenState) -> None:
        pass

    def get_injected_hydrogen(self) -> float:
        return self.injected_hydrogen

    def get_tank_pressure(self) -> float:
        return self.storage_pressure

    def get_soc(self) -> float:
        return 0

    def get_capacity(self) -> float:
        return 1000000


