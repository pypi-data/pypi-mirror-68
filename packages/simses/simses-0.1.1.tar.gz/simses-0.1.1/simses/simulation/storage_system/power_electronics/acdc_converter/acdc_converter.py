from abc import ABC, abstractmethod


class AcDcConverter(ABC):

    def __init__(self, max_power: float):
        self._MAX_POWER: float = max_power

    @abstractmethod
    def to_ac(self, power: float, voltage: float) -> float:
        """
        requested ac power in W, dc voltage level in V

        Parameters
        ----------
        power : float
        voltage : float

        Returns
        -------
        float
            dc power in W

        """
        pass

    @abstractmethod
    def to_dc(self, power: float, voltage: float) -> float:
        """
        requested ac power in W, dc voltage level in V

        Parameters
        ----------
        power : float
        voltage : float

        Returns
        -------
        float
            dc power in W

        """
        pass

    
    @abstractmethod
    def to_dc_reverse(self, dc_power: float) -> float:
        """
        recalculates ac power in W, if the BMS limits the DC_power

        Parameters
        ----------
        dc_power : float

        Returns
        -------
        float
            ac power in W

        """
        pass

    @abstractmethod
    def to_ac_reverse(self, dc_power: float) -> float:
        """
        recalculates ac power in W, if the BMS limits the DC_power

        Parameters
        ----------
        dc_power : float

        Returns
        -------
        float
            ac power in W

        """
        pass

    @property
    @abstractmethod
    def volume(self) -> float:
        """
        Volume of acdc converter in m3

        Returns
        -------

        """
        pass

    @property
    def max_power(self) -> float:
        """
        returns the maximum ac power of the acdc converter

        Parameters
        -------

        Returns
        -------
            float
                maximum power of the acdc converter (ac power)

        """
        return self._MAX_POWER

    @classmethod
    @abstractmethod
    def create_instance(cls, max_power: float, power_electronics_config: None):
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closing all open resources in acdc converter

        Parameters
        ----------

        Returns
        -------

        """
        pass
