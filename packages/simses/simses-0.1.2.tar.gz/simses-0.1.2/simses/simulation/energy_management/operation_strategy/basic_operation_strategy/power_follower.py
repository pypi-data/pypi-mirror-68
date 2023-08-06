from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy
from simses.commons.profile.power_profile.power_profile import PowerProfile


class PowerFollower(OperationStrategy):

    def __init__(self, power_profile: PowerProfile):
        super().__init__(OperationPriority.MEDIUM)
        self.__power_profile = power_profile

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        return -1 * self.__power_profile.next(time)

    def update(self, energy_management_state: EnergyManagementState) -> None:
        pass

    def close(self) -> None:
        self.__power_profile.close()
