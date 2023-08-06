from abc import ABC, abstractmethod

from simses.commons.timeseries.timevalue import TimeValue


class Average(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def average(self, data: [TimeValue]) -> float:
        pass
