import numpy as np
import math as m

from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage


class Pressuretank(HydrogenStorage):
    VAN_D_WAALS_COEF_A = 0.02452065  # van der Waals coefficient A of H2 (J*m³)/mol²
    VAN_D_WAALS_COEF_B = 2.65e-5  # van der Waals coefficient B of H2  m³/mol
    LHV_H2 = 33.327  # kWh/kg lower heating value H2
    MOLAR_MASS_H2 = 2.016  # g/mol
    IDEAL_GAS_CONST = 8.3145  # J/mol/K
    BOLTZ_CONST = 1.38e-23  # J/K
    TEMPERATURE = 273.15 + 25  # K
    __WALL_THIKNESS = 1  # cm

    def __init__(self, capacity: float, max_pressure: float, soc: float):
        super().__init__()
        self._soc = soc
        self.__capacity = capacity  # Wh
        self.__max_pressure = max_pressure  # bar

        self.__max_amount_hydrogen = self.calculate_max_amount_hydrogen()  # mol
        self.__volume = self.calculate_volume() * (100 * 100 * 100)  # cm3

        self.__diff_coef_wall = \
            4.4 * 10 ** (-7) * m.exp(
                -0.555 / self.BOLTZ_CONST / self.TEMPERATURE)  # cm2/s  selfdischarge through wall

        self.__inner_radius = (3 * self.__volume / (4 * m.pi)) ** (1 / 3)  # cm
        self.__inner_surface = 4 * m.pi * self.__inner_radius ** 2  # cm2

    def calculate_max_amount_hydrogen(self):
        """ returns max amount of hydrogen in mol that can be stored within the given pressuretank"""
        return self.__capacity / 1000 / (self.LHV_H2 * self.MOLAR_MASS_H2 /1000)

    def calculate_volume(self):
        """ returns required volume in m³ of the tank that represents the desired capacity """
        pressure = self.__max_pressure * 10**5
        a = 1
        b = - (self.__max_amount_hydrogen * self.VAN_D_WAALS_COEF_B + self.__max_amount_hydrogen * self.IDEAL_GAS_CONST \
               * self.TEMPERATURE / pressure)
        c = self.VAN_D_WAALS_COEF_A * self.__max_amount_hydrogen ** 2 / pressure
        d = - self.VAN_D_WAALS_COEF_B * self.VAN_D_WAALS_COEF_A * self.__max_amount_hydrogen ** 3 / pressure
        coeff = [a, b, c, d]
        n = np.roots(coeff)
        return np.max(np.real(n))

    def calculate_amount_hydrogen(self, soc: float):
        """ returns the current amount of hydrogen within the tank for a given SOC """
        return self.__max_amount_hydrogen * soc

    def calculate_hydrogen_concentration(self, soc: float):
        """ returns the current hydrogen concentration within the tank in mol/cm3 """
        return self.calculate_amount_hydrogen(soc) / self.__volume

    def ideal_gas_law(self, act_mass, volume):
        """ returns current pressure of the tank in Pa
            volume in m3, temperature in K, act_mass in mol """
        return act_mass * self.IDEAL_GAS_CONST * self.TEMPERATURE / (volume - act_mass * self.VAN_D_WAALS_COEF_B) - self.VAN_D_WAALS_COEF_A * act_mass ** 2 / volume ** 2  # pressure in Pa

    def diff_loss_wall(self, soc):
        """ returns mass losses caused by diffusion through the wall in mol/s """
        return self.__diff_coef_wall * self.calculate_hydrogen_concentration(soc) * self.__inner_surface / self.__WALL_THIKNESS

    def calculate_soc(self, time, state: HydrogenState) -> None:
        self._soc = state.soc + (state.hydrogen_production - state.hydrogen_use - self.diff_loss_wall(state.soc)) * (time - state.time) / self.__max_amount_hydrogen

    def get_soc(self):
        return self._soc

    def get_capacity(self):
        return self.__capacity

    def get_tank_pressure(self) -> float:
        soc = self._soc
        act_mass = self.calculate_amount_hydrogen(soc)
        volume = self.__volume / (100 * 100 * 100)  # cm³ -> m³
        return self.ideal_gas_law(act_mass, volume) / 10 ** 5  # pressure in bar
