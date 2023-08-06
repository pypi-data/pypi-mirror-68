from abc import ABC
import numpy as np


class ConstantsHydrogen(ABC):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    MOLAR_MASS_OXYGEN = 15.999 * 10 ** (-3)  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K
    HYDROGEN_HEAT_CAPACITY = 14304  # J/(kg K)
    OXYGEN_HEAT_CAPACITY = 920  # J/(kg K)
    DENSITY_WATER = 1000  # kg/m³
    EPS = np.finfo(float).eps
    LHV_H2 = 33.327  # kWh/kg lower heating value H2

    def __init__(self, max_pow_el, nom_pow_el, number_cells_el, geom_area_el, heat_capacity_el, max_pow_fc, nom_pow_fc,
                 number_cells_fc, geom_area_fc, heat_capacity_fc):
        super().__init__()

        self.MAXIMAL_POWER_ELECTROLYZER = max_pow_el
        self.NOMINAL_POWER_ELECTROLYZER = nom_pow_el
        self.NUMBER_CELLS_ELECTROLYZER = number_cells_el
        self.GEOM_AREA_ELECTROLYZER = geom_area_el
        self.HEAT_CAPACITY_ELECTROLZER = heat_capacity_el

        self.MAXIMAL_POWER_FUEL_CELL = max_pow_fc
        self.NOMINAL_POWER_FUEL_CELL = nom_pow_fc
        self.NUMBER_CELLS_FUEL_CELL = number_cells_fc
        self.GEOM_AREA_FUEL_CELL = geom_area_fc
        self.HEAT_CAPACITY_FUEL_CELL = heat_capacity_fc

    def get_max_power_el(self):
        return self.MAXIMAL_POWER_ELECTROLYZER

    def get_nom_power_el(self):
        return self.NOMINAL_POWER_ELECTROLYZER

    def get_number_cells_el(self):
        return self.NUMBER_CELLS_ELECTROLYZER

    def get_geom_area_el(self):
        return self.GEOM_AREA_ELECTROLYZER

    def get_heat_capacity_el(self):
        return self.HEAT_CAPACITY_ELECTROLZER

    def get_max_power_fc(self):
        return self.MAXIMAL_POWER_FUEL_CELL

    def get_nom_power_fc(self):
        return self.NOMINAL_POWER_FUEL_CELL

    def get_number_cells_fc(self):
        return self.NUMBER_CELLS_FUEL_CELL

    def get_geom_area_fc(self):
        return self.GEOM_AREA_FUEL_CELL

    def get_heat_capacity_fc(self):
        return self.HEAT_CAPACITY_FUEL_CELL