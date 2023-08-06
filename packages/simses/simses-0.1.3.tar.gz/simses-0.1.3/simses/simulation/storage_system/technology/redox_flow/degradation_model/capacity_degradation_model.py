from abc import ABC, abstractmethod

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState


class CapacityDegradationModel(ABC):
    def __init__(self):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)

    @abstractmethod
    def get_capacity_degradation(self, redox_flow_state: RedoxFlowState):
        pass
