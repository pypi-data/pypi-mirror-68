from abc import ABC, abstractmethod

from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary


class Pump(Auxiliary, ABC):
    """Pump is an auxiliary. It calculates the necessary pump power in W depending on the pressure losses."""
    def __init__(self):
        super().__init__()

    def ac_operation_losses(self) -> float:
        """
        Calculates the ac operation losses

        Parameters
        ----------

        Returns
        -------
        float:
            Power in W
        """
        return self.get_pump_power()

    @abstractmethod
    def calculate_pump_power(self, pressure_loss: float) -> None:
        """
        Calculates the pump power

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_pump_power(self) -> float:
        """
        Gets pump power in W

        Returns
        -------

        """
        pass

    @abstractmethod
    def set_eta_pump(self, flow_rate) -> float:
        """
        Sets pump efficiency

        Returns
        -------

        """
        pass
