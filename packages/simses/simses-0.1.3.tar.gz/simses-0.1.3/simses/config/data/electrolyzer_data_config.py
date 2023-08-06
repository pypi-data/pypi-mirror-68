from simses.constants_simses import ROOT_PATH
from simses.config.data.data_config import DataConfig


class ElectrolyzerDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'ELECTROLYZER_DATA'

    @property
    def pem_electrolyzer_lookuptabel_data_dir(self) -> str:
        """Returns directory of electrolyzer data files"""
        return ROOT_PATH + self.get_property(self.__section, 'ELECTROLYZER_LOOKUPTABLE_DATA_DIR')

    @property
    def pem_electrolyzer_parameters_data_dir(self) -> str:
        """Returns directory of electrolyzer data files"""
        return ROOT_PATH + self.get_property(self.__section, 'ELECTROLYZER_PARAMETERS_DATA_DIR')

    @property
    def pem_electrolyzer_pc_file(self) -> str:
        """Returns filename for polarisation curve for PEM-Electrolyzer"""
        return self.pem_electrolyzer_lookuptabel_data_dir + self.get_property(self.__section, 'PEM_ELECTROLYZER_PC_FILE')

    @property
    def pem_electrolyzer_power_file(self) -> str:
        """Returns filename for power curve for PEM-Electrolyzer"""
        return self.pem_electrolyzer_lookuptabel_data_dir + self.get_property(self.__section, 'PEM_ELECTROLYZER_POWER_FILE')

    @property
    def pem_electrolyzer_multi_dim_lookup_voltage_lookup_file(self) -> str:
        """Returns filename for polarisation curve for PEM-Electrolyzer"""
        return self.pem_electrolyzer_lookuptabel_data_dir + self.get_property(self.__section, 'PEM_ELECTROLYZER_MULTIDIM_LOOKUP_VOLTAGE_LOOKUP_FILE')

    @property
    def pem_electrolyzer_multidim_lookup_currentdensity_file(self) -> str:
        """Returns filename for power curve for PEM-Electrolyzer"""
        return self.pem_electrolyzer_lookuptabel_data_dir + self.get_property(self.__section, 'PEM_ELECTROLYZER_MULTIDIM_LOOKUP_CURRENTDENSITY_LOOKUP_FILE')

    @property
    def pem_electrolyzer_multi_dim_analytic_para_file(self) -> str:
        """Returns filename for power curve for PEM-Electrolyzer"""
        return self.pem_electrolyzer_parameters_data_dir + self.get_property(self.__section, 'PEM_ELECTROLYZER_MULTI_DIM_ANALYTIC_PARA_FILE')