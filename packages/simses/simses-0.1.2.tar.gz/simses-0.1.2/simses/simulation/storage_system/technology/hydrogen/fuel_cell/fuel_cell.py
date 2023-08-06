from abc import ABC, abstractmethod

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.water_heating.water_heating import WaterHeating


class FuelCell(ABC):

    FARADAY_CONST: float = 96485.3321  # As/mol

    def __init__(self):
        super().__init__()
        self.fuel_cell_pump = FixEtaCentrifugalPump(0.7)
        self.water_heating = WaterHeating()

    def update(self, time: float, state: HydrogenState, power, pressure_model, thermal_model) -> None:
        """
        Updates current, voltage and hydrogen flow of hydrogen state

        Parameters
        ----------
        state :

        Returns
        -------

        """
        self.calculate(power)
        state.current_fc = self.get_current()
        state.voltage_fc = self.get_voltage()
        state.hydrogen_use = self.get_hydrogen_consumption()

        # update temperature and pressure of the stack
        pressure_model.update(time, state)
        thermal_model.update(time, state)


    @abstractmethod
    def calculate(self, power) -> None:
        """
        Calculates current, voltage and hydrogen consumption based on input power
        Parameters
        ----------
        power : input power in W

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_current(self):
        """
        return electrical current in A

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_voltage(self):
        """
        Return of electrical voltage in V

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_hydrogen_consumption(self):
        """
        Return of hydrogen consumption in mol/s

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_nominal_stack_power(self):
        pass

    @abstractmethod
    def get_number_cells(self):
        pass

    @abstractmethod
    def get_geom_area_stack(self):
        pass

    @abstractmethod
    def get_heat_capactiy_stack(self):
        pass

    def get_auxiliaries_fuel_cell(self):
        return [self.fuel_cell_pump, self.water_heating]

    @abstractmethod
    def close(self):
        pass
