from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState


class HydrogenStorage(ABC):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K

    def __init__(self):
        super().__init__()

    def update(self, time: float, state: HydrogenState) -> None:
        """
        Update soc

        Parameters
        ----------
        state :

        Returns
        -------

        """
        self.calculate_soc(time, state)
        state.soc = self.get_soc()
        state.capacity = self.get_capacity()
        state.tank_pressure = self.get_tank_pressure()

    @abstractmethod
    def calculate_soc(self, time, state: HydrogenState) -> None:
        pass

    @abstractmethod
    def get_soc(self) -> float:
        pass

    @abstractmethod
    def get_capacity(self) -> float:
        pass

    @abstractmethod
    def get_tank_pressure(self) -> float:
        pass

