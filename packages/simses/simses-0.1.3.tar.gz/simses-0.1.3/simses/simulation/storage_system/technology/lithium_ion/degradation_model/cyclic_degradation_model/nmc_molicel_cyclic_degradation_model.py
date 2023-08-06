import math

from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.commons.log import Logger
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_molicel import MolicelNMC
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cyclic_degradation_model.\
    cyclic_degradation_model import CyclicDegradationModel


class MolicelNMCCyclicDegradationModel(CyclicDegradationModel):

    def __init__(self, cell_type:CellType, cycle_detector: CycleDetector):
        super().__init__(cell_type, cycle_detector)
        self.__log: Logger = Logger(type(self).__name__)
        self._cell: MolicelNMC = self._cell
        self.__capacity_loss = 0
        self.__capacity_loss_cyclic = 0
        self.__rinc_cyclic = 0
        self.__resistance_increase = 0

        self.__A_QLOSS = 1.1587  # constant
        self.__B_QLOSS = 1.569  # constant
        self.__C_QLOSS = 0.5562  # constant

        self.__A_RINC = 0.5562  # constant

        self.__cycle_detector: CycleDetector = cycle_detector

    def calculate_degradation(self, battery_state: LithiumIonState) -> None:
        crate: float = self.__cycle_detector.get_crate() * 3600 # in 1 / s -> *3600 -> in 1/h
        delta_fec: float = self.__cycle_detector.get_depth_of_full_cycle() # Delta EFC = DOC

        qloss: float = self.__capacity_loss_cyclic  # only cyclic losses
        qcell: float = battery_state.capacity / battery_state.nominal_voltage/ self._cell.get_parallel_scale()
        # single cell capacity in Ah

        if crate <= -0.5:
            k_capacity_cyc = self._cell.get_stressfkt_ca_cyc(delta_fec) / self.__A_QLOSS * (self.__A_QLOSS) \
                             ** (math.log2(crate / (-0.5)))
        elif abs(crate) < 0.5:
            k_capacity_cyc = self._cell.get_stressfkt_ca_cyc(delta_fec)
        else:
            k_capacity_cyc = self._cell.get_stressfkt_ca_cyc(delta_fec) * self.__B_QLOSS ** (math.log2(crate / 0.5))

        if k_capacity_cyc == 0.0:
            virtual_ChargeThroughput: float = 0
        else:
            virtual_ChargeThroughput: float = (qloss / k_capacity_cyc)**(1 / self.__C_QLOSS)

        capacity_loss = max(0,
                            k_capacity_cyc * (virtual_ChargeThroughput + delta_fec*qcell)**self.__C_QLOSS - qloss)

        self.__capacity_loss_cyclic += capacity_loss  # pu
        self.__capacity_loss = capacity_loss * self._cell.get_capacity()  # Ah

    def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
        delta_fec: float = self.__cycle_detector.get_depth_of_full_cycle() # Delta EFC = DOC

        rinc_cyclic: float = self.__rinc_cyclic
        k_ri_cyclic = self._cell.get_stressfkt_ri_cyc(delta_fec)
        if k_ri_cyclic == 0.0:
            virtual_ChargeThroughput: float = 0
        else:
            virtual_ChargeThroughput: float = (rinc_cyclic / k_ri_cyclic)**(1 / self.__A_RINC)

        qcell: float = battery_state.capacity / battery_state.nominal_voltage / self._cell.get_parallel_scale()
        # single cell capacity in Ah

        resistance_increase = max(0, k_ri_cyclic * (virtual_ChargeThroughput + delta_fec*qcell)\
                              **self.__A_RINC - self.__rinc_cyclic)


        self.__rinc_cyclic += resistance_increase
        self.__resistance_increase = resistance_increase  # pu

    def get_degradation(self) -> float:
        capacity_loss = self.__capacity_loss
        self.__capacity_loss = 0    # Set value to 0, because cyclic losses are not calculated in each step
        return capacity_loss

    def get_resistance_increase(self) -> float:
        resistance_increase = self.__resistance_increase
        self.__resistance_increase = 0 # Set value to 0, because cyclic losses are not calculated in each step
        return resistance_increase

    def reset(self, lithium_ion_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__capacity_loss_cyclic = 0
        self.__rinc_cyclic = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        self.__log.close()
