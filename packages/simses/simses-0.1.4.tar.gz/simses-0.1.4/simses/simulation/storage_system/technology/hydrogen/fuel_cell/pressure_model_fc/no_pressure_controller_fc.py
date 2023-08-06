from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.pressure_controller_fc import \
    PressureControllerFc


class NoPressureControllerFc(PressureControllerFc):

    def __init__(self):
        super().__init__()

    def calculate_n_h2_in(self, pressure_anode, pressure_anode_desire, n_h2_used) -> float:
        return n_h2_used

    def calculate_n_o2_in(self, pressure_cathode, pressure_cathode_desire, n_o2_used) -> float:
        return n_o2_used