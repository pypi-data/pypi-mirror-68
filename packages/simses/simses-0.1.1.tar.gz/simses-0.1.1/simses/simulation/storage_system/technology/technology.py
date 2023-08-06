from abc import ABC, abstractmethod

from simses.commons.state.technology.storage_technology_state import StorageTechnologyState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary


class StorageTechnology(ABC):
    """Abstract class for all technologies"""

    def __init__(self):
        pass

    @abstractmethod
    def distribute_and_run(self, time: float, current: float, voltage: float):
        """
        starts the update process of a data

        Parameters
        ----------
        time : current simulation time
        current : requested current for a data
        voltage : dc voltage for a data

        Returns
        -------

        """
        pass

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def get_auxiliaries(self) -> [Auxiliary]:
        pass

    @property
    @abstractmethod
    def state(self) -> StorageTechnologyState:
        """
        function to get the data state

        Parameters
        -------

        Returns
        -------
            StorageTechnologyState : specific data state

        """
        pass

    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Volume of storage technology in m3

        Returns
        -------

        """
        pass

    @abstractmethod
    def close(self):
        """
        Closing all open resources in a data

        Parameters
        ----------

        Returns
        -------

        """
        pass