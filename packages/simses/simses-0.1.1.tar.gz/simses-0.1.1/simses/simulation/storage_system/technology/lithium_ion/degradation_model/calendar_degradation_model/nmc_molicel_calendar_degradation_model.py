from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_molicel import MolicelNMC
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.calendar_degradation_model.\
    calendar_degradation_model import CalendarDegradationModel


class MolicelNMCCalendarDegradationModel(CalendarDegradationModel):

    # Values based on MA Ni Chuanqin (EES, TUM)

    def __init__(self, cell_type: CellType, general_config: GeneralSimulationConfig):
        super().__init__(cell_type)
        self._cell: MolicelNMC = self._cell
        self.__timestep: float = general_config.timestep
        self.__rinc_cal = 0
        self.__capacity_loss = 0
        self.__resistance_increase = 0
        self.__initial_capacity = self._cell.get_capacity()

    def calculate_degradation(self, battery_state: LithiumIonState) -> None:
        qloss = (self._cell.get_capacity() - battery_state.capacity / battery_state.nominal_voltage) / self.__initial_capacity # pu

        k_capacity_cal = self._cell.get_stressfkt_ca_cal(battery_state)
        virtual_time = (qloss/k_capacity_cal)**(4/3) # virtual aging time in weeks

        capacity_loss = k_capacity_cal*(virtual_time + self.__timestep/(86400*7))**0.75 - qloss # pu

        self.__capacity_loss = capacity_loss * self.__initial_capacity # Ah

    def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
        rinc_cal = self.__rinc_cal
        k_ri_cal = self._cell.get_stressfkt_ri_cal(battery_state)

        virtual_time = (rinc_cal/k_ri_cal)**2

        resistance_increase = k_ri_cal*(virtual_time + self.__timestep/(86400*7))**0.5 - rinc_cal
        self.__resistance_increase = resistance_increase  # pu
        self.__rinc_cal += resistance_increase

    def get_degradation(self) -> float:
        return self.__capacity_loss

    def get_resistance_increase(self) -> float:
        return self.__resistance_increase

    def reset(self, battery_state: LithiumIonState) -> None:
        self.__rinc_cal = 0
        self.__capacity_loss = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        pass
