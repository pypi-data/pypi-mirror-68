from simses.commons.state.system_state import SystemState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.dc_coupling.generation.dc_generation import DcGeneration
from simses.simulation.storage_system.dc_coupling.load.dc_load import DcLoad


class DcCoupling:

    def __init__(self, dc_load: DcLoad, dc_generation: DcGeneration):
        self.__dc_load: DcLoad = dc_load
        self.__dc_generation: DcGeneration = dc_generation

    def update(self, time: float, state: SystemState) -> None:
        self.__dc_load.calculate_power(time)
        self.__dc_generation.calculate_power(time)
        state.dc_power_additional += self.get_power()

    def get_power(self) -> float:
        return self.__dc_generation.get_power() - self.__dc_load.get_power()

    def get_auxiliaries(self) -> [Auxiliary]:
        auxiliaries: [Auxiliary] = list()
        auxiliaries.extend(self.__dc_load.get_auxiliaries())
        auxiliaries.extend(self.__dc_generation.get_auxiliaries())
        return auxiliaries

    def close(self):
        self.__dc_load.close()
        self.__dc_generation.close()