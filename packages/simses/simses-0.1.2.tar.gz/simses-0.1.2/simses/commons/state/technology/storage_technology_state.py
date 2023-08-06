from abc import ABC, abstractmethod

from simses.commons.state.state import State


class StorageTechnologyState(State, ABC):

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def is_charge(self) -> bool:
        """
        Returns True if current state presents a charging process, false otherwise

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def voltage(self) -> float:
        """
        DC Voltage in V

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def current(self) -> float:
        """
        DC Current in A

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def power_loss(self) -> float:
        """
        Power losses in W

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def soc(self) -> float:
        """
        SOC in p.u.

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def capacity(self) -> float:
        """
        Capacity in Wh

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def fulfillment(self) -> float:
        """
        Stage of power fulfillment of storage data in p.u.

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def convection_heat(self) -> float:
        """
        Heat transfer with system air in W

        Returns
        -------

        """
        pass
