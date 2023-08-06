from abc import abstractmethod, ABC

from simses.commons.state.technology.hydrogen_state import HydrogenState


class PressureModelEl(ABC):
    """
    PressureModelEl calculates the pressure development at the cathode of the electrolyzer in dependency of the
    hydrogenproductionrate, the hydrogenoutflow and the temperature
    """

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K

    def __init__(self):
        super().__init__()

    def update(self, time: float, hydrogen_state: HydrogenState):
        self.calculate(time, hydrogen_state)
        hydrogen_state.pressure_cathode_el = self.get_pressure_cathode_el()  # bar
        hydrogen_state.pressure_anode_el = self.get_pressure_anode_el()  # bar   anode pressure is not varied -> stays constant
        hydrogen_state.hydrogen_outflow = self.get_h2_outflow()
        hydrogen_state.oxygen_outflow = self.get_o2_outflow()
        hydrogen_state.water_outflow_cathode_el = self.get_h2o_outflow_cathode()
        hydrogen_state.water_outflow_anode_el = self.get_h2o_outflow_anode()

    @abstractmethod
    def calculate(self, time, hydrogen_state: HydrogenState) -> None:
        pass

    @abstractmethod
    def get_pressure_cathode_el(self) -> float:
        pass

    @abstractmethod
    def get_pressure_anode_el(self) -> float:
        pass

    @abstractmethod
    def get_h2_outflow(self) -> float:
        pass

    @abstractmethod
    def get_o2_outflow(self) -> float:
        pass

    @abstractmethod
    def get_h2o_outflow_cathode(self) -> float:
        pass

    @abstractmethod
    def get_h2o_outflow_anode(self) -> float:
        pass

    def close(self) -> None:
        """ Closing all resources in pressure model """
        pass