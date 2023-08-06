from abc import ABC, abstractmethod

from simses.commons.state.state import State


class PowerDistributor(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def set(self, states: [State]) -> None:
        pass

    @abstractmethod
    def get_power_for(self, power: float, state: State):
        pass
