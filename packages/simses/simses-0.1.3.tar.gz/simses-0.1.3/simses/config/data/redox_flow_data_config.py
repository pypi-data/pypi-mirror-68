from simses.constants_simses import ROOT_PATH
from simses.config.data.data_config import DataConfig


class RedoxFlowDataConfig(DataConfig):

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'REDOX_FLOW_DATA'

    @property
    def redox_flow_data_dir(self) -> str:
        """Returns directory of redox flow data files"""
        return ROOT_PATH + self.get_property(self.__section, 'REDOX_FLOW_DATA_DIR')

    @property
    def rfb_rint_file(self) -> str:
        """Returns filename for internal resistance of a RFB stack"""
        return self.redox_flow_data_dir + self.get_property(self.__section, 'RFB_RINT_FILE')
