import math as m

import numpy as np
import pandas as pd

from simses.commons.log import Logger
from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.data.parameters.parameters_pem_electrolyzer_multi_dim_analytic import \
    ParametersPemElectrolyzerMultiDimAnalytic
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer


class PemElectrolyzerMultiDimAnalytic(Electrolyzer):
    """An PEM-Electrolyzer is a special typ of an Electrolyzer"""
    EPS = np.finfo(float).eps

    def __init__(self, electrolyzer_maximal_power: float, electrolyzer_data_config: ElectrolyzerDataConfig):
        super().__init__()
        # constants cell
        self.__parameters = ParametersPemElectrolyzerMultiDimAnalytic(electrolyzer_data_config)
        self.GEOM_AREA_CELL = 1225  # cm2  example from Siemens from: PEM-Elektrolyse-Systeme zur Anwendung in Power-to-Gas Anlagen
        self.NOM_POWER_CELL = 5000  # W   side length = 35 cm
        self.MAX_POWER_CELL = 7962.5  # W  based on polarizationscurve model from: PEM-Elektrolyse-Systeme zur Anwendung in Power-to-Gas Anlagen
        self.RATIO_NOM_TO_MAX = self.NOM_POWER_CELL / self.MAX_POWER_CELL
        self.MEM_THIKNESS = 200 * 10 ** (-4)  # cm
        self.MAX_CURRENTDENSITY_CELL = 3  # A/cm2
        self.MIN_CURRENTDENSITY_CELL = 0  # A/cm2
        self.NOM_VOLTAGE_CELL = 2  # V
        self.A_CATHODE = 2.4  # bar cm²/A
        self.A_ANODE = 2.8  # bar cm²/A
        self.R_ELE = 0.096  # Ohm cm²
        self.P_H2_REF = 1  # bar
        self.P_O2_REF = 1  # bar
        self.__log: Logger = Logger(type(self).__name__)
        # TODO Review: With this calculation you adapt the maximum power -> you need to adapt maximum power and inform the user you adapted it
        if electrolyzer_maximal_power < self.MAX_POWER_CELL:
            self.__NUMBER_CELLS = 1
        else:
            self.__NUMBER_CELLS = round(electrolyzer_maximal_power / self.MAX_POWER_CELL)
        self.MAXIMAL_STACK_POWER = self.__NUMBER_CELLS * self.MAX_POWER_CELL
        self.__NOMINAL_STACK_POWER = self.RATIO_NOM_TO_MAX * self.MAXIMAL_STACK_POWER
        self.__log.info('maximal stack power of electrolyzer was adapted to: ' + str(self.MAXIMAL_STACK_POWER))
        self.__log.info('nominal stack power of electrolyzer is: ' + str(self.__NOMINAL_STACK_POWER))
        self.__log.info('number of serial cells is: ' + str(self.__NUMBER_CELLS))
        self.__GEOM_AREA_STACK = self.__NUMBER_CELLS * self.GEOM_AREA_CELL
        self.HEAT_CAPACITY_STACK = 4933 * self.__NOMINAL_STACK_POWER / 1000  # J/K, c = 4933 J/K/kW from: Operational experience and Control strategies for a stand-alone power system based on renewable energy and hydrogen

        # constants membrane
        self.DIFF_COEF_H2 = 4.65 * 10 ** (-11)  # mol/(cm s bar)
        self.DIFF_COEF_O2 = 2 * 10 ** (-11)  # mol/(cm s bar)
        self.WATER_DRAG_COEFF = 0.27  # molH20/ molH+
        self.LAMBDA = 25  # degree of humidification

        # parameters of curve fitting currentdensity
        self.__q1 = self.__parameters.get_corr_parameter_q1()
        self.__q2 = self.__parameters.get_corr_parameter_q2()
        self.__q3 = self.__parameters.get_corr_parameter_q3()
        self.__q5 = self.__parameters.get_corr_parameter_q5()
        self.__q11 = self.__parameters.get_corr_parameter_q11()
        self.__q12 = self.__parameters.get_corr_parameter_q12()
        self.__q13 = self.__parameters.get_corr_parameter_q13()
        self.__q14 = self.__parameters.get_corr_parameter_q14()
        self.__q15 = self.__parameters.get_corr_parameter_q15()
        self.__q16 = self.__parameters.get_corr_parameter_q16()
        self.__q18 = self.__parameters.get_corr_parameter_q18()
        self.__q20 = self.__parameters.get_corr_parameter_q20()
        self.__q22 = self.__parameters.get_corr_parameter_q22()
        self.__q23 = self.__parameters.get_corr_parameter_q23()
        self.__q24 = self.__parameters.get_corr_parameter_q24()
        self.__q25 = self.__parameters.get_corr_parameter_q25()

        # parameters of curve fitting of activation powerdensity
        self.__p00 = self.__parameters.get_act_pow_parameter_p00()
        self.__p10 = self.__parameters.get_act_pow_parameter_p10()
        self.__p01 = self.__parameters.get_act_pow_parameter_p01()
        self.__p20 = self.__parameters.get_act_pow_parameter_p20()
        self.__p11 = self.__parameters.get_act_pow_parameter_p11()
        self.__p02 = self.__parameters.get_act_pow_parameter_p02()

        # import of correction parameters for analytic currentdensity calculation
        self.__PARA_FILE = electrolyzer_data_config.pem_electrolyzer_multi_dim_analytic_para_file
        self.correction_parameters = pd.read_csv(self.__PARA_FILE, delimiter=';', decimal=",")
        self.corr_params = self.correction_parameters.iloc[:, 0]

        # initial values
        # TODO Review: Please ensure that you only define necessary member variables here. Do not use local as member variables!
        self.__current_stack = 0  # A
        self.__voltage_stack = 0  # V
        self.__sat_pressure_h2o = 0.03189409713071401  # bar
        self.__part_pressure_h2 = 1 - self.__sat_pressure_h2o  # bar
        self.__part_pressure_o2 = 1 - self.__sat_pressure_h2o # bar
        self.__h2_generation_stack = 0  # mol/s
        self.__o2_generation_stack = 0  # mol/s
        self.__h2o_use_stack = 0  # mol/s

    def calculate(self, power: float, temperature: float, pressure_anode: float, pressure_cathode: float):
        # TODO Review: Why do you rename the variables? Units should be fixed via docstring in superclass
        stack_temperature = temperature - 273.15  # K -> °C
        power_dens_cell = power / self.__NUMBER_CELLS / self.GEOM_AREA_CELL  # W/cm2

        # calculation of current, partial pressures and cell voltage at cell level
        current_dens_cell = self.calculate_current_denstiy(stack_temperature, pressure_anode, pressure_cathode, power_dens_cell)  # A/cm2
        # TODO Review: Here you set member variables. Better: Have distinct methods for each and return the value as a local variable
        # self.calculate_partial_pressures(stack_temperature, pressure_anode, pressure_cathode, current_dens_cell)
        self.__sat_pressure_h2o = self.calculate_sat_pressure_h2o(stack_temperature)
        self.__part_pressure_h2 = self.calculate_part_pressure_h2(self.__sat_pressure_h2o, pressure_cathode, current_dens_cell)
        self.__part_pressure_o2 = self.calculate_part_pressure_o2(self.__sat_pressure_h2o, pressure_anode, current_dens_cell)
        voltage_cell = self.calculate_cell_voltage(stack_temperature, current_dens_cell)  # V
        current_cell = current_dens_cell * self.GEOM_AREA_CELL  # A

        # calculation of current and voltage at stack level
        self.__voltage_stack = voltage_cell * self.__NUMBER_CELLS  # V  cells are serial connected to one stack
        self.__current_stack = current_cell  # A  cells are serial connected to a Stack

        # generation and use of water, hydrogen and oxygen
        h2_generation_cell = current_cell / (2 * ConstantsHydrogen.FARADAY_CONST)  # mol/s
        o2_generation_cell = current_cell / (4 * ConstantsHydrogen.FARADAY_CONST)  # mol/s
        h2o_use_cell = current_cell / (2 * ConstantsHydrogen.FARADAY_CONST)  # mol/s

        # permeation of hydrogen and oxygen through membrane due to diffusion because of differential partial pressures
        if self.__part_pressure_h2 + self.__sat_pressure_h2o <= 1 + self.EPS:  # prevention of negative pressure at cathode side
            h2_permeation_cell = 0
            o2_permeation_cell = 0
        else:
            h2_permeation_cell = self.DIFF_COEF_H2 * self.__part_pressure_h2 / self.MEM_THIKNESS  # mol/s  permeation of hydrogen due to differential partial pressure of hydrogen at cathode and anode
            if current_cell > 0:
                o2_permeation_cell = self.DIFF_COEF_O2 * self.__part_pressure_o2 / self.MEM_THIKNESS  # mol/s permeation of oxygen due to differential partial pressure of oxygen at anode and cathode
            else:
                o2_permeation_cell = 0  # prevention of negative pressure at anode side in case of no current flow -> no oxygen production
        h2o_permeation_cell = self.WATER_DRAG_COEFF * current_cell / ConstantsHydrogen.FARADAY_CONST  # water beeing draged by protons through the membrane

        # net mass balance Cathode at cell level
        h2_net_cathode = h2_generation_cell - h2_permeation_cell - 2 * o2_permeation_cell
        h2o_net_cathode = h2o_permeation_cell + 2 * o2_permeation_cell

        # net mass balance Anode at cell level
        o2_net_anode = o2_generation_cell - o2_permeation_cell
        h2o_net_anode = - h2o_use_cell - h2o_permeation_cell

        # net use of water, production of hydrogen and oxygen at Stack level
        self.__h2o_use_stack = - (h2o_net_anode + h2o_net_cathode) * self.__NUMBER_CELLS
        self.__o2_generation_stack = o2_net_anode * self.__NUMBER_CELLS
        self.__h2_generation_stack = h2_net_cathode * self.__NUMBER_CELLS

    def calculate_current_denstiy(self, stack_temperature, p_anode, p_cathode, power_dens_cell):
        # TODO Review: Please define an own class for the fitting parameters and have getters for each

        # TODO Review: Please have those functions in separate private methods -> small, readable and understandable chunks

        sat_p_h2o = self.calculate_sat_pressure_h2o(stack_temperature, self.__q11, self.__q12, self.__q13, self.__q14)
        p_h2 = self.calculate_part_pressure_h2(sat_p_h2o, p_cathode, 0, self.__q15)
        p_o2 = self.calculate_part_pressure_o2(sat_p_h2o, p_anode, 0, self.__q16)

        u_rev = self.calculate_rev_voltage(stack_temperature, self.__q1, self.__q2, self.__q3, self.__q5)  # V
        u_nernst = self.calculate_nernst_voltage(stack_temperature, u_rev, p_h2, p_o2, self.__q20)
        r_mem = self.calculate_mem_resistance(stack_temperature)  # Ohm cm²
        r_ohm = self.__q18 * self.R_ELE + r_mem

        # TODO Review: solving the following equation is actually the focus of this method -> try to set the focus on this

        # coefficients for solving quadratic equation
        A = r_ohm + self.__p20
        B = u_nernst + self.__p10 + self.__q22 * self.__p11 * stack_temperature
        C = self.__q23 * self.__p00 + self.__q24 * self.__p01 * stack_temperature + self.__q25 * self.__p02 * stack_temperature ** 2 - power_dens_cell

        # calculation of currentdensity
        if power_dens_cell == 0:
            return 0
        else:
            return (- B + (B ** 2 - 4 * A * C) ** (1 / 2)) / (2 * A)

    def calculate_cell_voltage(self, stack_temperature, current_dens):

        # TODO Review: Please define distinct (private) methods for each voltage calculation

        # nerst voltage
        u_rev = self.calculate_rev_voltage(stack_temperature)
        u_nernst = self.calculate_nernst_voltage(stack_temperature, u_rev, self.__part_pressure_h2,
                                                 self.__part_pressure_o2)

        # Activation-voltage
        u_act = self.calculate_act_voltage(stack_temperature, current_dens)

        # ohmic voltage
        r_mem = self.calculate_mem_resistance(stack_temperature)
        u_ohm = (r_mem + self.R_ELE) * current_dens  # V

        # addition of overpotentials is cellvoltage
        return u_nernst + u_act + u_ohm

    def calculate_rev_voltage(self, stack_temperature, q1: float=1, q2: float=1, q3: float=1, q5: float=1) -> float:
        return q1 * 1.5184 - q2 * 1.5421 * 10 ** (-3) * (stack_temperature + 273.15) + q3 * 9.523 * 10 ** (-5) * \
               (stack_temperature + 273.15) * np.log((stack_temperature + 273.15)) + q5 * 9.84 * 10 ** (-8) * \
               (stack_temperature + 273.15) ** 2  # from "Hydrogen science and engeneering: Materials, processed, systems.."

    def calculate_nernst_voltage(self, stack_temperature, u_rev, p_h2, p_o2, q20: float=1) -> float:
        return u_rev + q20 * ConstantsHydrogen.IDEAL_GAS_CONST * (stack_temperature + 273.15) / \
               (2 * ConstantsHydrogen.FARADAY_CONST) * np.log((p_o2 / self.P_O2_REF) ** (1 / 2) * p_h2 / self.P_H2_REF)

    def calculate_act_voltage(self, stack_temperature, current_dens) -> float:
        alpha = 0.6627 * m.exp(-0.187 * stack_temperature) + 0.02934 * m.exp(-0.00454 * stack_temperature)  # V
        i_0 = 0.002159 * m.exp(-0.3179 * stack_temperature) + 1.149 * 10 ** (-7) * m.exp(
            -0.0205 * stack_temperature)  # A
        if current_dens == 0:
            return 0  # V
        else:
            return alpha * m.log(current_dens / i_0)  # V

    def calculate_mem_resistance(self, stack_temperature) -> float:
        conductivity_nafion = (0.005139 * self.LAMBDA - 0.00326) * \
                              np.exp(1268 * (1 / (303) - 1 / (stack_temperature + 273.15)))  # S/cm 0.14
        return self.MEM_THIKNESS / conductivity_nafion

    def calculate_sat_pressure_h2o(self, stack_temperature, q11: float=1, q12: float=1, q13: float=1, q14: float=1) -> float:
        return 10 ** (-2.1794 * q11 + q12 * 0.02953 * stack_temperature - q13 * 9.1837 * 10 ** (-5) * stack_temperature ** 2
                      + q14 * 1.4454 * 10 ** (-7) * stack_temperature ** 3)  # bar saturationpressure of water

    def calculate_part_pressure_h2(self, sat_pressure_h2o, p_cathode, current_dens_cell, q15: float=1) -> float:
        return (1 + q15 * p_cathode) - sat_pressure_h2o + self.A_CATHODE * current_dens_cell # bar

    def calculate_part_pressure_o2(self, sat_pressure_h2o, p_anode, current_dens_cell, q16: float=1) -> float:
        return (1 + q16 * p_anode) - sat_pressure_h2o + self.A_ANODE * current_dens_cell  # bar

    # TODO Review: Please privatize all following member variables -> self.__current_stack instead of self.current_stack

    def get_current(self):
        # print('the current is: ' + str(self.__current) + ' mA')
        return self.__current_stack

    def get_hydrogen_production(self):
        # print('the massflow of hydrogen ist: ' + str(self.__hydrogen_generation) + ' mol/s')
        return self.__h2_generation_stack

    def get_oxygen_production(self):
        return self.__o2_generation_stack

    def get_voltage(self):
        # print('the voltage is: ' + str(self.__voltage) + ' V')
        return self.__voltage_stack

    def get_water_use(self):
        return self.__h2o_use_stack

    def get_number_cells(self):
        return self.__NUMBER_CELLS

    def get_geom_area_stack(self):
        return self.__GEOM_AREA_STACK

    def get_nominal_stack_power(self):
        return self.__NOMINAL_STACK_POWER

    def get_heat_capacity_stack(self):
        return self.HEAT_CAPACITY_STACK

    def get_partial_pressure_h2(self):
        return self.__part_pressure_h2

    def get_partial_pressure_o2(self):
        return self.__part_pressure_o2

    def get_sat_pressure_h2o(self):
        return self.__sat_pressure_h2o

    def close(self):
        self.__log.close()


