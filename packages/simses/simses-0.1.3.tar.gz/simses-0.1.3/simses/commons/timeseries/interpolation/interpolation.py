from abc import ABC, abstractmethod

from simses.commons.timeseries.timevalue import TimeValue


class Interpolation(ABC):

    def __init__(self):
        super().__init__()

    @staticmethod
    def is_necessary(tstmp: float, data: [TimeValue]) -> bool:
        if len(data) > 1:
            return data[-2].time < tstmp < data[-1].time
        return False

    @abstractmethod
    def interpolate(selfself, time: float, recent: TimeValue, last: TimeValue) -> float:
        pass
