import math

import pandas as pd
import scipy.interpolate
from numpy import asarray

from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.data.battery_data_config import BatteryDataConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType


class PanasonicNCA(CellType):
    """An NCA (PanasonicNCR) is a special cell type and inherited by CellType"""

    __SOC_HEADER = 'SOC'
    __SOC_IDX = 0
    __OCV_IDX = 1
    __TEMP_IDX = 1
    __C_RATE_IDX = 0
    __ETA_IDX = 1

    __CELL_VOLTAGE = 3.6  # V
    __CELL_CAPACITY = 2.73  # Ah

    pd.set_option('precision', 9)

    def __init__(self, voltage: float, capacity: float, battery_data_config: BatteryDataConfig, battery_config: BatteryConfig):
        super().__init__(voltage, capacity, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__OCV_FILE = battery_data_config.nca_panasonicNCR_ocv_file
        self.__RINT_FILE = battery_data_config.nca_panasonicNCR_rint_file
        self.__nom_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = 4.2 * self._SERIAL_SCALE  # V
        self.__min_voltage = 2.5 * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah
        self.__max_c_rate_charge = 0.5  # 1/h
        self.__max_c_rate_discharge = 3.5  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A
        self.__min_temperature = 273.15  # K
        self.__max_temperature = 318.15  # K

        self.__coulomb_efficiency = 1  # Coulomb Efficiency is set to 1. Losses are calculated via internal resistance

        self.__self_discharge_rate = 0  # Self discharge is neglectged in our simulations;
        # self.__self_discharge_rate = 0.015 / (30.5 * 24 * 3600)  # 1.5%-soc per month in second step

        # Physical parameters for lithium_ion thermal model
        self.__mass = 0.044  # kg
        self.__diameter = 18  # mm
        self.__length = 65  # mm
        self.__volume = math.pi * self.__diameter ** 2 * self.__length / 4 * 10 ** (-9)  # m3
        self.__surface_area = (2 * math.pi * self.__diameter / 2 * self.__length + 2 * math.pi * (
                self.__diameter / 2) ** 2) * 10 ** (-6)  # m2
        self.__specific_heat = 0  # J/kgKpanasonic
        self.__convection_coefficient = 15  # W/m2K, parameter for natural convection
        # (source: https://www.akkuteile.de/lithium-ionen-akkus/18650/panasonic/panasonic-ncr18650_100605_1206)

        self.__open_circuit_voltage = pd.read_csv(self.__OCV_FILE, delimiter=';', decimal=",")  # V
        self.__internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm

        self.soc_arr = self.__internal_resistance.iloc[:, self.__SOC_IDX]
        self.temp_arr = self.__internal_resistance.iloc[:4, self.__TEMP_IDX]

        self.rint_mat_ch = self.__internal_resistance.iloc[:, 2]
        self.rint_mat_dch = self.__internal_resistance.iloc[:, 5]
        self.__rint_interp1d_ch = scipy.interpolate.interp1d(self.soc_arr, self.rint_mat_ch, kind='linear')
        self.__rint_interp1d_dch = scipy.interpolate.interp1d(self.soc_arr, self.rint_mat_dch, kind='linear')

        self.__log.debug('soc arr size: ' + str(len(self.soc_arr)) + ', temp arr size: ' + str(
            len(self.temp_arr.T)) + ', rint ch mat size: ' + str(asarray(self.rint_mat_ch).shape))
        self.__log.debug('soc arr size: ' + str(len(self.soc_arr)) + ', temp arr size: ' + str(
            len(self.temp_arr.T)) + ', rint dch mat size: ' + str(asarray(self.rint_mat_dch).shape))

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        soc = battery_state.soc
        soc_idx = abs(self.__open_circuit_voltage[self.__SOC_HEADER] - soc).idxmin()
        # get the idex of the row which has the closest value to current soc value, but
        # problematic if soc table has lower resolution
        return self.__open_circuit_voltage.iat[soc_idx, self.__OCV_IDX] * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        soc = battery_state.soc

        if battery_state.is_charge:
            # internal resistance for charge
            res = self.__rint_interp1d_ch(soc)
            self.__log.debug('res charging: ' + str(res / self._PARALLEL_SCALE * self._SERIAL_SCALE))
            return float(res / self._PARALLEL_SCALE * self._SERIAL_SCALE)
        else:
            # internal resistance for discharge
            res = self.__rint_interp1d_dch(soc)
            self.__log.debug('res discharging: ' + str(res / self._PARALLEL_SCALE * self._SERIAL_SCALE))
            return float(res / self._PARALLEL_SCALE * self._SERIAL_SCALE)

    def get_self_discharge_rate(self) -> float:
        return self.__self_discharge_rate

    def get_coulomb_efficiency(self, battery_state: LithiumIonState) -> float:
        return self.__coulomb_efficiency if battery_state.is_charge else 1 / self.__coulomb_efficiency

    def get_nominal_voltage(self) -> float:
        return self.__nom_voltage

    def get_min_current(self, battery_state: LithiumIonState) -> float:
        return self.__min_current

    def get_capacity(self) -> float:
        return self.__capacity

    def get_max_current(self, battery_state: LithiumIonState) -> float:
        return self.__max_current

    def get_min_temp(self) -> float:
        return self.__min_temperature

    def get_max_temp(self) -> float:
        return self.__max_temperature

    def get_min_voltage(self) -> float:
        return self.__min_voltage

    def get_max_voltage(self) -> float:
        return self.__max_voltage

    def get_serial_scale(self) -> float:
        return self._SERIAL_SCALE

    def get_parallel_scale(self) -> float:
        return self._PARALLEL_SCALE

    # Physical parameters for lithium_ion thermal model

    def get_mass(self) -> float:
        return self.__mass * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_volume(self):
        return self.__volume * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_surface_area(self):
        return self.__surface_area * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def close(self):
        self.__log.close()
