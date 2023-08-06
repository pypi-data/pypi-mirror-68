from simses.commons.profile.technical_profile.soc_profile import SocProfile
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig
from simses.simulation.energy_management.operation_strategy.operation_priority import OperationPriority
from simses.simulation.energy_management.operation_strategy.operation_strategy import OperationStrategy


class SocFollower(OperationStrategy):

    def __init__(self, config: GeneralSimulationConfig, profile_config: ProfileConfig):
        super().__init__(OperationPriority.MEDIUM)
        self.__soc_profile = SocProfile(profile_config)
        self.__timestep = config.timestep
        self.__Wh_to_Ws = 3600

    def next(self, time: float, system_state: SystemState, power: float = 0) -> float:
        soc_dif = self.__soc_profile.next() - system_state.soc
        capacity_dif = soc_dif * system_state.capacity * self.__Wh_to_Ws
        return capacity_dif / self.__timestep

    def update(self, energy_management_state: EnergyManagementState) -> None:
        pass

    def close(self) -> None:
        self.__soc_profile.close()
