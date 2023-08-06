from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.auxiliary.compressor.hydrogen_isentrop_compressor import \
    HydrogenIsentropCompressor
from simses.simulation.storage_system.auxiliary.gas_drying.hydrogen_gas_drying import HydrogenGasDrying
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.pressure_model_el import \
    PressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model_el.thermal_model_el import ThermalModelEl
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump


class Electrolyzer(ABC):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K
    DENSITY_WATER = 1000  # kg/m³

    def __init__(self):
        super().__init__()
        self.electrolyzer_pump = FixEtaCentrifugalPump(0.7)
        self.gas_drying = HydrogenGasDrying()
        self.compressor = HydrogenIsentropCompressor(0.95)
        self.water_heating = WaterHeating()
        self.storage_pressure = 200  # barg
        self.convection_heat_el = 0  # W

    def update(self, time: float, state: HydrogenState, power: float, pressure_model: PressureModelEl, thermal_model: ThermalModelEl) -> None:
        """
        Updates hydrogen states that are corrolated with the electrolyzer such as current, voltage, hydrogen production,
        water use and temperature

        Parameters
        ----------
        state :

        Returns
        -------

        """
        self.calculate(power, state.temperature_el, state.pressure_anode_el, state.pressure_cathode_el)
        state.current_el = self.get_current()
        state.voltage_el = self.get_voltage()
        state.hydrogen_production = self.get_hydrogen_production()
        state.oxygen_production = self.get_oxygen_production()
        state.water_use = self.get_water_use()
        state.part_pressure_h2_el = self.get_partial_pressure_h2()
        state.part_pressure_o2_el = self.get_partial_pressure_o2()
        state.sat_pressure_h2o_el = self.get_sat_pressure_h2o()

        # state values that will be needed before they were updated
        pressure_cathode_0 = state.pressure_cathode_el  # barg
        pressure_anode_0 = state.pressure_anode_el  # barg
        temperature_0 = state.temperature_el  # K

        # update temperature and pressure of the stack
        pressure_model.update(time, state)
        state.water_use += state.water_outflow_cathode_el + state.water_outflow_anode_el
        thermal_model.update(time, state, pressure_cathode_0, pressure_anode_0)
        self.convection_heat_el = thermal_model.get_convection_heat()

        # update auxilliary losses
        state.power_water_heating_el = thermal_model.get_power_water_heating()
        state.power_pump_el = thermal_model.get_pump_power()
        timestep = time - state.time
        self.gas_drying.calculate_gas_drying_power(pressure_cathode_0, state.hydrogen_outflow, timestep)
        state.power_gas_drying = self.gas_drying.get_gas_drying_power()
        self.compressor.calculate_compression_power(state.hydrogen_outflow, pressure_cathode_0+1, self.storage_pressure, temperature_0)
        state.power_compressor = self.compressor.get_compression_power()

    def get_auxiliaries_electrolyzer(self):
        return [self.gas_drying, self.compressor, self.water_heating, self.electrolyzer_pump]

    def get_convection_heat_el(self) -> float:
        return self.convection_heat_el

    @abstractmethod
    def calculate(self, power: float, temperature: float, pressure_anode: float, pressure_cathode: float) -> None:
        """
        Calculates current, voltage and hydrogen generation based on input power

        Parameters
        ----------
        power : input power in W
        temperature: temperature of electrolyzer in K
        pressure_anode: relative pressure on anode side of electrolyzer in barg (relative to 1 bar)
        pressure_cathode: relative pressure on cathode side of electrolyzer in barg (relative to 1 bar)

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_current(self):
        """
        return electrical current of the electrolyzer stack in A

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_voltage(self):
        """
        Return of electrical voltage of electrolyzer stack in V

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_hydrogen_production(self):
        """
        Return of total hydrogen generation of the stack in mol/s

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_oxygen_production(self):
        """
        Return of total oxygen generation of the stack in mol/s

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_water_use(self):
        """
        Return of water use of electrolyzer stack at anode side

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_number_cells(self):
        """
        Returns number of serial electrolyseur cells
        -------

        """
        pass

    @abstractmethod
    def get_geom_area_stack(self):
        """
        Returns geometric area of one cell
        -------

        """
        pass

    @abstractmethod
    def get_nominal_stack_power(self):
        """
        Returns nominal_stack_power of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_heat_capacity_stack(self):
        """
        Returns nominal_stack_power of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_partial_pressure_h2(self):
        """
        Returns partial pressure of hydrogen at cathode side of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_partial_pressure_o2(self):
        """
        Returns partial pressure of oxigen at anode side of electrolyzer
        -------

        """
        pass

    @abstractmethod
    def get_sat_pressure_h2o(self):
        """
        Returns staturation pressure of h2o for given temperature
        -------

        """
        pass

    @abstractmethod
    def close(self):
        pass
