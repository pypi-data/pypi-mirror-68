from abc import ABC, abstractmethod

from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary


class DcLoad(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_power(self) -> float:
        pass

    @abstractmethod
    def calculate_power(self, time: float) -> None:
        pass

    @abstractmethod
    def get_auxiliaries(self) -> [Auxiliary]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
