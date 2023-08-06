from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.simulation.energy_management_config import EnergyManagementConfig
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy
from simses.commons.profile.power_profile.power_profile import PowerProfile


class PeakShaving(OperationStrategy):
    ''' Basic Peak Shaving operation strategy: If the storage is almost full (> xy %),
    the storage is not charged anymore to avoid a misrepresent fulfillmentfactor
    '''

    def __init__(self, power_profile: PowerProfile, ems_config: EnergyManagementConfig):
        super().__init__(OperationPriority.VERY_HIGH)
        self.__load_profile = power_profile
        self.__max_power: float = ems_config.max_power
        self.__power = 0
        self.__soc_threshold = 1

    def next(self, time: float, system_state: SystemState, power_offset: float = 0) -> float:
        self.__power = self.__load_profile.next(time)
        net_load = (self.__power + power_offset) - self.__max_power
        if system_state.soc >= self.__soc_threshold and net_load < 0:
            return 0
        else:
            return -1 * net_load

    def update(self, energy_management_state: EnergyManagementState) -> None:
        energy_management_state.load_power = self.__power

    def close(self) -> None:
        self.__load_profile.close()
