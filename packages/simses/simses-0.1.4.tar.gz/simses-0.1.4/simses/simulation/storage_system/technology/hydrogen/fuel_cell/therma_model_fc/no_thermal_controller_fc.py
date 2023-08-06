from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.thermal_controller_fc import \
    ThermalControllerFc


class NoThermalControllerFc(ThermalControllerFc):

    def __init__(self):
        super().__init__()

    def calculate_water_flow(self, stack_temperature, max_water_flow_cell, min_water_flow_cell) -> float:
        return 0

    def calculate_water_temperature_in(self, stack_temperature) -> float:
        return stack_temperature