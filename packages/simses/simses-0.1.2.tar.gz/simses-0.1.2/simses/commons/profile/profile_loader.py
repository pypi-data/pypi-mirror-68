from configparser import ConfigParser

from simses.simulation.energy_management.energy_management_factory import EnergyManagementFactory


class ProfileLoader:
    """
    loads specific profiles for post processing(e.g. analysis)
    """
    def __init__(self, config: ConfigParser, path: str):
        self.__ems_factory: EnergyManagementFactory = EnergyManagementFactory(config, path)
        self.__pv_profile = self.__ems_factory.generation_profile()

    def load_profile_data(self) -> list:
        """
        Returns the load profile as a list

        Parameters
        ----------

        Returns
        -------
        list
            load profile
        """

        __load_profile = self.__ems_factory.load_profile()
        __load = __load_profile.profile_data_to_list(sign_factor=-1)
        return __load

    def pv_profile_data(self) -> list:
        """
        Returns the pv profile as a list

        Parameters
        ----------

        Returns
        -------
        list
            pv profile
        """

        return self.__pv_profile.profile_data_to_list(sign_factor=1)

    def get_fcr_data(self) -> list:
        """
        Returns the frequency as a list

        Parameters
        ----------

        Returns
        -------
        list
            frequency profile
        """

        pass
