from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.no_pressure_controller_el import \
    NoPressureControllerEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.pressure_model_el import \
    PressureModelEl


class NoPressureModelEl(PressureModelEl):

    def __init__(self):
        super().__init__()
        self.__pressure_cathode_el = 0  # barg
        self.__pressure_anode_el = 0  # barg
        self.__pressure_cathode_desire_el = 0  # barg
        self.__pressure_anode_desire_el = 0  # barg
        self.__hydrogen_outflow = 0  # mol/s
        self.__oxygen_outflow = 0  # mol/s
        self.pressure_controller = NoPressureControllerEl()

    def calculate(self, time, hydrogen_state: HydrogenState) -> None:
        self.__pressure_anode_el = hydrogen_state.pressure_anode_el
        self.__pressure_cathode_el = hydrogen_state.pressure_cathode_el
        hydrogen_produced = hydrogen_state.hydrogen_production
        oxygen_produced = hydrogen_state.oxygen_production
        self.__hydrogen_outflow = self.pressure_controller.calculate_n_h2_out(self.__pressure_cathode_el, self.__pressure_cathode_desire_el, hydrogen_produced, 0)
        self.__oxygen_outflow = self.pressure_controller.calculate_n_o2_out(self.__pressure_anode_el, self.__pressure_anode_desire_el, oxygen_produced)

    def get_pressure_anode_el(self) -> float:
        return self.__pressure_anode_el

    def get_pressure_cathode_el(self) -> float:
        return self.__pressure_cathode_el

    def get_h2_outflow(self) -> float:
        return self.__hydrogen_outflow

    def get_o2_outflow(self) -> float:
        return self.__oxygen_outflow


