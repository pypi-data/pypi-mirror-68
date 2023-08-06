from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState


class ThermalModelEl(ABC):
    #
    # MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    # FARADAY_CONST: float = 96485.3321  # As/mol
    # IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    # HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    # MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    # HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    # HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K


    def __init__(self):
        self.max_water_flow_cell = 0  # mol/s/cell

    def update(self, time: float, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        """Updating temperature of electrolyzer stack in hydrogen state"""
        self.calculate(time, hydrogen_state, pressure_cathode_0, pressure_anode_0)
        hydrogen_state.water_flow_el = self.get_water_flow_stack()
        self.calculate_pump_power(hydrogen_state.water_flow_el)
        hydrogen_state.temperature_el = self.get_temperature()


    @abstractmethod
    def calculate(self, time: float, hydrogen_state: HydrogenState, pressure_cathode_0, pressure_anode_0) -> None:
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        pass

    @abstractmethod
    def get_water_flow_stack(self) -> float:
        pass

    @abstractmethod
    def get_power_water_heating(self) -> float:
        pass

    @abstractmethod
    def calculate_pump_power(self, water_flow_stack: float) -> None:
        pass

    @abstractmethod
    def get_pump_power(self) -> float:
        pass

    @abstractmethod
    def get_convection_heat(self) -> float:
        pass

    def close(self) -> None:
        """Closing all resources in thermal model"""
        pass
