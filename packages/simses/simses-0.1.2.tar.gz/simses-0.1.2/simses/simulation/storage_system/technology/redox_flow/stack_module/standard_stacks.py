from math import log10

import pandas as pd
import scipy.interpolate
from numpy import asarray

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class StandardStack(StackModule):
    """A stack is part of a stack module, Stacks can be connected serial of parallel to a stack module."""

    __SOC_IDX = 0

    __CELL_VOLTAGE_NOM = 1.4  # V
    __CELL_NUMBER = 40  # -
    __STACK_VOLTAGE_NOM = __CELL_VOLTAGE_NOM * __CELL_NUMBER  # V
    __STACK_POWER_NOM = 5600  # W
    __CELL_AREA = 2160  # cm^2
    __SELF_DISCHARGE_CURRENT_DENS = 0.1  # mA/cm²

    def __init__(self, voltage: float, power: float, redox_flow_data_config: RedoxFlowDataConfig):
        super().__init__(voltage, power, self.__STACK_VOLTAGE_NOM, self.__STACK_POWER_NOM)

        self.__FARADAY = 96485  # As/mol
        self.__concentration_v = 1600  # mol/m³

        self.__log: Logger = Logger(__name__)
        self.__RINT_FILE = redox_flow_data_config.rfb_rint_file

        pd.set_option('precision', 9)

        self.__number_cells_stack = self.__CELL_NUMBER  # -
        self.__flow_rate = 0.2 * 2160 / 1000000 / 60 * self.__number_cells_stack * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m³/s

        self.__max_voltage = 1.6 * self.__number_cells_stack * self._SERIAL_SCALE  # V
        self.__min_voltage = 1.0 * self.__number_cells_stack * self._SERIAL_SCALE  # V
        self.__nom_voltage_cell = self.__CELL_VOLTAGE_NOM  # V

        self.__temperature = 303.15  # K
    #     # Temperature range for standard vanadium electrolyte (1.6 M V, 2 M H2SO4)
    #     self.__min_temperature = 283.15  # K
    #     self.__max_temperature = 313.15  # K

        self.__self_discharge_current = self.__SELF_DISCHARGE_CURRENT_DENS * self.__CELL_AREA * self.__number_cells_stack * self._SERIAL_SCALE * self._PARALLEL_SCALE / 1000 # A
        self.__stacks_volume = self.__CELL_AREA * self.__number_cells_stack * self._SERIAL_SCALE * self._PARALLEL_SCALE * 0.37 * 0.9 / 1000000  # m³

        self.__internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm
        self.__soc_arr = self.__internal_resistance.iloc[:, self.__SOC_IDX]
        self.__rint_mat_ch = self.__internal_resistance.iloc[:, 3]
        self.__rint_mat_dch = self.__internal_resistance.iloc[:, 6]

    def get_open_circuit_voltage(self, ocv_cell) -> float:
        return ocv_cell * self.__number_cells_stack * self._SERIAL_SCALE

    def get_internal_resistance(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        soc_arr = self.__soc_arr

        if redox_flow_state.is_charge:
            # internal resistance for charge
            rint_mat_ch = self.__rint_mat_ch
            self.__log.debug('soc arr size: ' + str(len(soc_arr)) + ', rint mat size: ' +
                             str(asarray(rint_mat_ch).shape))
            rint_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_ch, kind='linear')
            self.__log.debug('after interpolation of charging')
            res = rint_interp1d(soc)
            self.__log.debug('res charging stack: ' + str(res))
            self.__log.debug('res charging: ' + str(res / self._PARALLEL_SCALE * self._SERIAL_SCALE))
            return float(res / self._PARALLEL_SCALE * self._SERIAL_SCALE)
        else:
            # internal resistance for discharge
            rint_mat_dch = self.__rint_mat_dch
            self.__log.debug('soc arr size: ' + str(len(soc_arr)) + ', rint mat size: ' +
                             str(asarray(rint_mat_dch).shape))
            rint_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_dch, kind='linear')
            self.__log.debug('after interpolation of discharging')
            res = rint_interp1d(soc)
            self.__log.debug('res discharging stack: ' + str(res))
            self.__log.debug('res discharging: ' + str(res / self._PARALLEL_SCALE * self._SERIAL_SCALE))
            return float(res / self._PARALLEL_SCALE * self._SERIAL_SCALE)

    def get_cell_per_stack(self):
        return self.__number_cells_stack

    def get_min_voltage(self) -> float:
        return self.__min_voltage

    def get_max_voltage(self) -> float:
        return self.__max_voltage

    def get_min_current(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        min_current = -soc * self.__FARADAY * self.__concentration_v * self.__flow_rate / self._SERIAL_SCALE / self.__number_cells_stack / self._PARALLEL_SCALE
        return min_current

    def get_max_current(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        max_current = (1 - soc) * self.__FARADAY * self.__concentration_v * self.__flow_rate / self._SERIAL_SCALE / self.__number_cells_stack /self._PARALLEL_SCALE
        return max_current

    #   def get_viscosity_anolyte(self, redox_flow_state: RedoxFlowState) -> float:
    #     # source: Fink, Holger. Untersuchung von Verlustmechanismen in Vanadium-Flussbatterien. Diss. Technische Universität München, 2019.
    #     viscosity = 0.0006115 * exp(2785/self.__temperature)-(3.765 - 0.068 * (self.__temperature-273.15-10)) * (redox_flow_state.soc - 0.2)  # mPas
    #     return viscosity
    #
    # def get_viscosity_catholyte(self, redox_flow_state: RedoxFlowState) -> float:
    #     # source: Fink, Holger. Untersuchung von Verlustmechanismen in Vanadium-Flussbatterien. Diss. Technische Universität München, 2019.
    #     viscosity = 0.0005702 * exp(2680/self.__temperature)-(1.337 - 0.031 * (self.__temperature-273.15-10)) * (redox_flow_state.soc - 0.2)  # mPas
    #     return viscosity

    def get_self_discharge_current(self, redox_flow_state: RedoxFlowState) -> float:
        return self.__self_discharge_current

    def get_stacks_volume(self):
        return self.__stacks_volume

    def get_nominal_voltage_cell(self) -> float:
        return self.__nom_voltage_cell

    def get_electrolyte_temperature(self) -> float:
        return self.__temperature

    def get_specif_cell_area(self):
        return self.__CELL_AREA

    def close(self):
        super().close()
        self.__log.close()
