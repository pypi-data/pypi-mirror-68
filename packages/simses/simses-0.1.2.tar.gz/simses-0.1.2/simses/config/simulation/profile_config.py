import os
from configparser import ConfigParser

from constants_simses import ROOT_PATH
from simses.commons.profile.power_profile.file_power_profile import FilePowerProfile
from simses.commons.profile.utils import get_header_from
from simses.config.simulation.simulation_config import SimulationConfig


class ProfileConfig(SimulationConfig):

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        # self.__log: Logger = Logger(type(self).__name__)
        self.__section: str = 'PROFILE'

    @property
    def power_profile_dir(self) -> str:
        """Returns directory of power profiles from __analysis_config file_name"""
        path = self.get_property(self.__section, 'POWER_PROFILE_DIR')
        if self._is_absolute_path(path):
            return path
        else:
            return ROOT_PATH + path

    @property
    def technical_profile_dir(self) -> str:
        """Returns directory of frequency profiles from __analysis_config file_name"""
        path = self.get_property(self.__section, 'TECHNICAL_PROFILE_DIR')
        if self._is_absolute_path(path):
            return path
        else:
            return ROOT_PATH + path

    @property
    def load_profile(self) -> str:
        """ Return selected load profile name from __analysis_config file_name"""
        return self.power_profile_dir + self.get_property(self.__section, 'LOAD_PROFILE')

    @property
    def frequency_file(self) -> str:
        """Returns frequency profile file_name name from __analysis_config file_name"""
        return self.technical_profile_dir + self.get_property(self.__section, 'FREQUENCY_PROFILE')

    @property
    def load_forecast_file(self) -> str:
        """Returns frequency profile file_name name from __analysis_config file_name"""
        return self.technical_profile_dir + self.get_property(self.__section, 'LOAD_FORECAST_PROFILE')

    @property
    def soc_file(self) -> str:
        """Returns soc profile file_name name from __analysis_config file_name"""
        return self.technical_profile_dir + self.get_property(self.__section, 'SOC_PROFILE')

    @property
    def pv_generation_profile_file(self) -> str:
        """ Return PV generation profile file_name name from __analysis_config file_name"""
        return self.power_profile_dir + self.get_property(self.__section, 'PV_GENERATION_PROFILE')

    @property
    def load_scaling_factor(self) -> float:
        """ Return scaling factor for the load from __analysis_config file_name"""
        load_scaling_factor: float = float(self.get_property(self.__section, 'LOAD_SCALING_FACTOR'))
        if load_scaling_factor == 1.0:
            return load_scaling_factor  # default value 1: original values are taken
        else:
            return load_scaling_factor / 1000.0 / self.__get_annual_consumption()

    @property
    def pv_scaling_factor(self) -> float:
        """ Return scaling factor for pv from __analysis_config file_name"""
        pv_scaling_factor: float = float(self.get_property(self.__section, 'PV_SCALING_FACTOR'))
        if pv_scaling_factor == 1.0:
            return pv_scaling_factor  # deafult value 1: original values are taken
        else:
            return pv_scaling_factor / 1000.0 / self.__get_pv_peak_power()

    def __get_annual_consumption(self) -> float:
        return self.__get_value_from_header(FilePowerProfile.Header.ANNUAL_CONSUMPTION, self.load_profile)

    def __get_pv_peak_power(self) -> float:
        return self.__get_value_from_header(FilePowerProfile.Header.PEAK_POWER, self.pv_generation_profile_file)

    @staticmethod
    def __get_value_from_header(name: str, file: str) -> float:
        try:
            header: dict = get_header_from(file)
            value = float(header[name])
            return value
        except IndexError:
            return 1.0

    @staticmethod
    def _is_absolute_path(path: str) -> bool:
        return os.path.isabs(path)
