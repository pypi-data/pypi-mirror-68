import math

import pandas as pd
import scipy.interpolate

from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.data.battery_data_config import BatteryDataConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType


class MolicelNMC(CellType):
    """An NMC (NMC_Molicel) is a special cell type and inherited by CellType"""

    __SOC_HEADER = 'SOC'
    __SOC_IDX = 0
    __DOC_IDX = 0
    __OCV_IDX = 1
    __TEMP_IDX = 1
    __C_RATE_IDX = 0
    __ETA_IDX = 1
    __LENGTH_TEMP_ARRAY = 40
    __LENGTH_SOC_ARRAY = 1001
    __LENGTH_DOC_ARRAY = 1001

    __CELL_VOLTAGE = 3.7  # V
    __CELL_CAPACITY = 1.9  # Ah

    pd.set_option('precision', 9)

    def __init__(self, voltage: float, capacity: float, battery_data_config: BatteryDataConfig, battery_config: BatteryConfig):
        super().__init__(voltage, capacity, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__OCV_FILE = battery_data_config.nmc_molicel_ocv_file
        self.__RINT_FILE = battery_data_config.nmc_molicel_rint_file
        self.__CAPACITY_CAL_FILE = battery_data_config.nmc_molicel_capacity_cal_file
        self.__RI_CAL_FILE = battery_data_config.nmc_molicel_ri_cal_file
        self.__CAPACITY_CYC_FILE = battery_data_config.nmc_molicel_capacity_cyc_file
        self.__RI_CYC_FILE = battery_data_config.nmc_molicel_ri_cyc_file
        self.__nom_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = 4.25 * self._SERIAL_SCALE  # V
        self.__min_voltage = 3 * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah

        self.__max_c_rate_charge = 1.05  # 1/h
        self.__max_c_rate_discharge = 2.1  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A

        self.__min_temperature = 273.15  # K
        self.__max_temperature = 318.15  # K

        self.__coulomb_efficiency_charge = 1  # -
        self.__coulomb_efficiency_discharge = 1  # -
        self.__self_discharge_rate = 0 # Self discharge is neglectged in our simulations;
        # self.__self_discharge_rate = 0.015 / (30.5 * 24 * 3600)  # 1.5%-soc per month in second step

        # Physical parameters for lithium_ion thermal model
        self.__mass = 0.05 * self._SERIAL_SCALE * self._PARALLEL_SCALE  # in kg for 1 cell
        self.__diameter = 18  # mm
        self.__length = 65  # mm
        self.__volume = math.pi * self.__diameter ** 2 * self.__length / 4 * 10 ** (-9) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m3
        self.__surface_area = (2 * math.pi * self.__diameter / 2 * self.__length + 2 * math.pi * (
                    self.__diameter / 2) ** 2) * 10 ** (-6) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m2
        self.__specific_heat = 823  # J/kgK
        # Source for specific_heat: https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2004/046721.pdf )
        self.__convection_coefficient = 15  # W/m2K, parameter for natural convection

        self.__open_circuit_voltage = pd.read_csv(self.__OCV_FILE, delimiter=';', decimal=",")  # V

        capacity_cyc = pd.read_csv(self.__CAPACITY_CYC_FILE, delimiter=';', decimal=",")  # -
        capacity_cyc_mat = capacity_cyc.iloc[:self.__LENGTH_DOC_ARRAY, 1]
        doc_arr = capacity_cyc.iloc[:, self.__DOC_IDX]
        self.__capacity_cyc_interp1d = scipy.interpolate.interp1d(doc_arr, capacity_cyc_mat, kind='linear')

        ri_cyc = pd.read_csv(self.__RI_CYC_FILE, delimiter=';', decimal=",")  # -
        ri_cyc_mat = ri_cyc.iloc[:(self.__LENGTH_DOC_ARRAY + 1), 1]
        doc_arr = ri_cyc.iloc[:, self.__DOC_IDX]
        self.__ri_cyc_interp1d = scipy.interpolate.interp1d(doc_arr, ri_cyc_mat, kind='linear')

        internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm
        soc_arr = internal_resistance.iloc[:, self.__SOC_IDX]
        temp_arr = internal_resistance.iloc[:4, self.__TEMP_IDX]
        rint_mat_ch = internal_resistance.iloc[:, 2]
        rint_mat_dch = internal_resistance.iloc[:, 5]
        self.__rint_ch_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_ch, kind='linear')
        self.__rint_dch_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_dch, kind='linear')

        capacity_cal = pd.read_csv(self.__CAPACITY_CAL_FILE, delimiter=';', decimal=",")  # -
        capacity_cal_mat = capacity_cal.iloc[:(self.__LENGTH_TEMP_ARRAY + 1), 2:]
        soc_arr = capacity_cal.iloc[:, self.__SOC_IDX]
        temp_arr = capacity_cal.iloc[:(self.__LENGTH_TEMP_ARRAY + 1), self.__TEMP_IDX]
        self.__capacity_cal_interp1d = scipy.interpolate.interp2d(soc_arr, temp_arr.T, capacity_cal_mat, kind='linear')

        ri_cal = pd.read_csv(self.__RI_CAL_FILE, delimiter=';', decimal=",")  # -
        ri_cal_mat = ri_cal.iloc[:(self.__LENGTH_TEMP_ARRAY + 1), 2:]
        soc_arr = ri_cal.iloc[:, self.__SOC_IDX]
        temp_arr = ri_cal.iloc[:(self.__LENGTH_TEMP_ARRAY + 1), self.__TEMP_IDX]
        self.__ri_cal_interp1d = scipy.interpolate.interp2d(soc_arr, temp_arr.T, ri_cal_mat, kind='linear')

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        soc = battery_state.soc
        soc_idx = abs(self.__open_circuit_voltage[self.__SOC_HEADER] - soc).idxmin()
        # get the idex of the row which has the closest value to current soc value, but
        # problematic if soc table has lower resolution
        return self.__open_circuit_voltage.iloc[soc_idx, self.__OCV_IDX] * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        if battery_state.is_charge:
            rint = self.__rint_ch_interp1d(battery_state.soc)
        else:
            rint = self.__rint_dch_interp1d(battery_state.soc)
        return float(rint) / self._PARALLEL_SCALE * self._SERIAL_SCALE

    def get_stressfkt_ca_cal(self, battery_state: LithiumIonState) -> float:
        """
        get the stress factor for calendar aging capacity loss

        Parameters
        ----------
        battery_state :

        Returns
        -------

        """
        return float(self.__capacity_cal_interp1d(battery_state.soc, battery_state.temperature))

    def get_stressfkt_ri_cal(self, battery_state: LithiumIonState) -> float:
        """
        get the stress factor for calendar aging capacity loss

        Parameters
        ----------
        battery_state :

        Returns
        -------

        """
        return float(self.__ri_cal_interp1d(battery_state.soc, battery_state.temperature))

    def get_stressfkt_ca_cyc(self, doc: float) -> float:
        return float(self.__capacity_cyc_interp1d(doc))

    def get_stressfkt_ri_cyc(self, doc: float) -> float:
        return float(self.__ri_cyc_interp1d(doc))

    def get_self_discharge_rate(self) -> float:
        return self.__self_discharge_rate

    def get_coulomb_efficiency(self, battery_state: LithiumIonState) -> float:
        return self.__coulomb_efficiency_charge if battery_state.is_charge else 1 / self.__coulomb_efficiency_discharge

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

    def get_mass(self) -> float:
        return self.__mass

    def get_volume(self):
        return self.__volume

    def get_surface_area(self):
        return self.__surface_area

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def close(self):
        self.__log.close()
