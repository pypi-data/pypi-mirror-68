from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model_el.thermal_controller_el import \
    ThermalControllerEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model_el.thermal_model_el import ThermalModelEl


class SimpleThermalController(ThermalControllerEl):
    """ This controller controlls the temperature of the EL-stack by setting new values for the mass flow and the
    temperature of the water running through one cell. It is asumed that the water temperature coming out of the
    stack equals the stack temperature"""

    def __init__(self):
        super().__init__()
        self.stack_temp_desire = 75  # K
        self.water_flow_cell = 0  # mol/s
        self.delta_water_temperature = 5  # K
        self.controll_faktor_temperature_neg = 1/5
        self.controll_faktor_temperature_pos = 1/5

    def calculate_water_flow(self, temperature_stack, max_water_flow_cell, min_water_flow_cell) -> float:   # water_use due to chemical reactin is neglected here
        if temperature_stack <= self.stack_temp_desire:
            return min_water_flow_cell
        else:
            return max_water_flow_cell

    def calculate_water_temperature_in(self, temperature_water_out) -> float:
        temp_diff = temperature_water_out - self.stack_temp_desire
        controll_faktor = self.calculate_control_faktor_temperature(temp_diff)
        if temperature_water_out <= self.stack_temp_desire:
            return temperature_water_out + controll_faktor * self.delta_water_temperature
        else:
            return temperature_water_out - controll_faktor * self.delta_water_temperature

    def calculate_control_faktor_temperature(self, temp_diff):
        if temp_diff < 0 and temp_diff > -5:
            return - self.controll_faktor_temperature_neg * temp_diff
        if temp_diff >= 0 and temp_diff < 5:
            return self.controll_faktor_temperature_pos * temp_diff
        else:
            return 1
