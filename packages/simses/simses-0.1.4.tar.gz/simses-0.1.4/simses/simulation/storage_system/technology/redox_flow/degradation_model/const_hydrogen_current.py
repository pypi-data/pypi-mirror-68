from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class ConstHydrogenCurrent(CapacityDegradationModel):
    def __init__(self, stack_module: StackModule, general_config: GeneralSimulationConfig):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__timestep: float = general_config.timestep
        self.__stack_module = stack_module
        self.__hydrogen_current_density = 2.5 * 10**-6  # A/cm^2
        self.__hydrogen_current = (self.__hydrogen_current_density * self.__stack_module.get_cell_per_stack() *
                                   self.__stack_module.get_serial_scale() * self.__stack_module.get_parallel_scale() *
                                   self.__stack_module.get_specif_cell_area())
        self.__log.debug('The hydrogen generation current is: ' + str(self.__hydrogen_current))

    def get_capacity_degradation(self, redox_flow_state: RedoxFlowState):
        return self.__hydrogen_current * self.__timestep * self.__stack_module.get_nominal_voltage_cell() / 3600  # Wh
