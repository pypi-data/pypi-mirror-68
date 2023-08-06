from configparser import ConfigParser

from simses.config.simulation.simulation_config import SimulationConfig, create_dict_from, create_list_from, clean_split


class StorageSystemConfig(SimulationConfig):

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'STORAGE_SYSTEM'

    @property
    def storage_systems_dc(self) -> [[str]]:
        """Returns a list of dc storage systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_SYSTEM_DC'))
        return create_list_from(props)

    @property
    def storage_systems_ac(self) -> [[str]]:
        """Returns a list of ac storage systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_SYSTEM_AC'))
        return create_list_from(props)

    @property
    def acdc_converter(self) -> dict:
        """Returns a list of acdc converter"""
        props: [str] = clean_split(self.get_property(self.__section, 'ACDC_CONVERTER'))
        return create_dict_from(props)

    @property
    def hvac(self) -> dict:
        """Returns a list of hvac systems"""
        props: [str] = clean_split(self.get_property(self.__section, 'HVAC'))
        return create_dict_from(props)

    @property
    def storage_technologies(self) -> dict:
        """Returns a list of storage technologies"""
        props: [str] = clean_split(self.get_property(self.__section, 'STORAGE_TECHNOLOGY'))
        return create_dict_from(props)

    @property
    def ambient_temperature_model(self) -> str:
        """Returns name of ambient temperature model"""
        return self.get_property(self.__section, 'AMBIENT_TEMPERATURE_MODEL')

    @property
    def cycle_detector(self) -> str:
        """Returns name of cycle detector"""
        return self.get_property(self.__section, 'CYCLE_DETECTOR')
