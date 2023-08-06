import pandas as pd

from simses.commons.log import Logger
from simses.config.data.electrolyzer_data_config import ElectrolyzerDataConfig
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer


class PemElectrolyzer(Electrolyzer):
    """An PEM-Electrolyzer is a special typ of an Electrolyzer"""

    __POWER_HEADER = 'cellpower at 1 bar'
    __VOLTAGE_IDX = 1
    __POWER_IDX = 1
    __CURRENT_IDX = 0
    __GEOM_AREA = 50  # cm2
    __POWER = 100  # W

    def __init__(self, electrolyzer_maximal_power: float, electrolyzer_data_config: ElectrolyzerDataConfig):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__SPEC_MAX_POWER = 10.8  # W/cm2
        self.__NOMINAL_STACK_POWER = electrolyzer_maximal_power
        self.__GEOM_AREA = electrolyzer_maximal_power / self.__SPEC_MAX_POWER
        self.__NUMBER_CELLS = 1
        self.__PC_FILE = electrolyzer_data_config.pem_electrolyzer_pc_file
        self.__POWER_FILE = electrolyzer_data_config.pem_electrolyzer_power_file
        self.__MAX_CURRENT_DENSITY = 5  # A/cm2
        self.__MIN_CURRENT_DENSITY = 0  # mA
        self.__polarization_curve = pd.read_csv(self.__PC_FILE, delimiter=';', decimal=",")  # V/(mA/cm2)
        self.__power_curve = pd.read_csv(self.__POWER_FILE, delimiter=';', decimal=",")  # W/cm2
        self.__current_arr = self.__polarization_curve.iloc[:, self.__CURRENT_IDX] * self.__GEOM_AREA  # mA
        self.__polarization_arr = self.__polarization_curve.iloc[:, self.__VOLTAGE_IDX]  # V
        self.__power_arr = self.__power_curve.iloc[:, self.__POWER_IDX] * self.__GEOM_AREA  # W
        self.__part_pressure_h2 = 0.526233372104
        self.__part_pressure_o2 = 0.526233372104
        self.__sat_pressure_h2o = 0.466925594058
        self.__heat_capacity = 4933 * self.__NOMINAL_STACK_POWER / 1000  # J/K, c = 4933 J/K/kW from: Operational experience and Control strategies for a stand-alone power system based on renewable energy and hydrogen

    def calculate(self, power: float, temperature: float, pressure_anode: float, pressure_cathode: float):
        power_idx = abs(self.__power_curve[self.__POWER_HEADER] * self.__GEOM_AREA - power).idxmin()
        self.__voltage = self.__polarization_curve.iloc[power_idx, self.__VOLTAGE_IDX]  # V
        self.__current = self.__power_curve.iloc[power_idx, self.__CURRENT_IDX] * self.__GEOM_AREA  # mA
        self.__hydrogen_generation = self.__current / (2 * Electrolyzer.FARADAY_CONST)  # mol/s

    def get_current(self):
        # print('the current is: ' + str(self.__current) + ' mA')
        return self.__current

    def get_hydrogen_production(self):
        # print('the massflow of hydrogen ist: ' + str(self.__hydrogen_generation) + ' mol/s')
        return self.__hydrogen_generation

    def get_oxygen_production(self):
        return self.__hydrogen_generation / 2

    def get_voltage(self):
        # print('the voltage is: ' + str(self.__voltage) + ' V')
        return self.__voltage

    def get_water_use(self):
        return self.__hydrogen_generation  # water use is the same as hydrogen generation

    def get_number_cells(self):
        return self.__NUMBER_CELLS

    def get_nominal_stack_power(self):
        return self.__NOMINAL_STACK_POWER

    def get_heat_capacity_stack(self):
        return self.__heat_capacity

    def get_partial_pressure_h2(self):
        return self.__part_pressure_h2

    def get_partial_pressure_o2(self):
        return self.__part_pressure_o2

    def get_sat_pressure_h2o(self):
        return self.__sat_pressure_h2o

    def get_geom_area_stack(self):
        return self.__GEOM_AREA

    def close(self):
        self.__log.close()


