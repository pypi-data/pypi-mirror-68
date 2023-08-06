from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import CapacityDegradationModel


class NoDegradation(CapacityDegradationModel):
    def __init__(self):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)

    def get_capacity_degradation(self, redox_flow_state: RedoxFlowState):
        return 0.0
