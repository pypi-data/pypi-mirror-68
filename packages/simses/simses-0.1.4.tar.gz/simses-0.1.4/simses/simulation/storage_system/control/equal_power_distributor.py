from simses.commons.state.state import State
from simses.simulation.storage_system.control.power_distributor import PowerDistributor


class EqualPowerDistributor(PowerDistributor):

    def __init__(self, number: float):
        super().__init__()
        self.__number: float = number

    def set(self, states: [State]) -> None:
        pass

    def get_power_for(self, power: float, state: State) -> float:
        return power / self.__number
