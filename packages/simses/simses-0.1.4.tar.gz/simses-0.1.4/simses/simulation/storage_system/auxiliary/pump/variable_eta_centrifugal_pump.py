import pandas as pd
import scipy.interpolate
import numpy as np

from simses.commons.log import Logger
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.config.data.auxiliary_data_config import AuxiliaryDataConfig


class VariableEtaCentrifugalPump(Pump):

    def __init__(self, auxiliary_data_config: AuxiliaryDataConfig):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__power = 0
        self.__eta = 0
        self.__ETA_FILE = auxiliary_data_config.pump_eta_file
        self.__efficiency = pd.read_csv(self.__ETA_FILE, delimiter=',', decimal=".", header=None, index_col=0)
        self.__flow_rate_arr = self.__efficiency.iloc[0] * 10 ** -3 / 60  # m^3/s
        self.__eta_arr = self.__efficiency.iloc[1]/100
        self.__efficiency_interp1d = scipy.interpolate.interp1d(self.__flow_rate_arr, self.__eta_arr, kind='linear')

    def calculate_pump_power(self, pressure_loss) -> None:
        if pressure_loss == 0:
            self.__power = 0
        else:
            self.__power = pressure_loss / self.__eta

    def set_eta_pump(self, flow_rate):
        self.__eta = self.__efficiency_interp1d(flow_rate)
        self.__log.debug('Pump Efficiency is ' + str(self.__eta))

    def get_pump_power(self) -> float:
        return self.__power
