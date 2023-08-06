from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.no_pressure_controller_fc import \
    NoPressureControllerFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.pressure_model_fc import \
    PressureModelFc


class NoPressureModelFc(PressureModelFc):

    def __init__(self):
        super().__init__()
        self.__pressure_cathode_fc = 0  # barg
        self.__pressure_anode_fc = 0  # barg
        self.__pressure_cathode_desire_fc = 0  # barg
        self.__pressure_anode_desire_fc = 0  # barg
        self.__hydrogen_inflow = 0  # mol/s
        self.__oxygen_inflow = 0  # mol/s
        self.pressure_controller = NoPressureControllerFc()

    def calculate(self, time, hydrogen_state: HydrogenState) -> None:
        self.__pressure_anode_fc = hydrogen_state.pressure_anode_fc
        self.__pressure_cathode_fc = hydrogen_state.pressure_cathode_fc
        hydrogen_used = hydrogen_state.hydrogen_use
        oxygen_used = hydrogen_state.oxygen_use
        self.__hydrogen_inflow = self.pressure_controller.calculate_n_h2_in(self.__pressure_anode_fc, self.__pressure_anode_desire_fc, hydrogen_used)
        self.__oxygen_inflow = self.pressure_controller.calculate_n_o2_in(self.__pressure_cathode_fc, self.__pressure_cathode_desire_fc, oxygen_used)

    def get_pressure_cathode_fc(self) -> float:
        return self.__pressure_cathode_fc

    def get_pressure_anode_fc(self) -> float:
        return self.__pressure_anode_fc

    def get_h2_inflow(self) -> float:
        return self.__hydrogen_inflow

    def get_o2_inflow(self) -> float:
        return self.__oxygen_inflow


