from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.pressure_model_el import \
    PressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.var_cathode_pressure_controller_el import \
    VarCathodePressureControllerEl


class VarCathodePressureModelEl(PressureModelEl):


    def __init__(self, constants: ConstantsHydrogen):
        super().__init__()
        self.__pressure_controller = VarCathodePressureControllerEl()
        self.__constants = constants
        self.VOLUME_GAS_SEPARATOR = 500 / (100 * 100)  # cm² -> m²  #TODO(JK) different Volume for different power of electrolyzerstack
        self.electrolyzer_nom_power = self.__constants.get_nom_power_el()
        self.p_c_1 = 0  # barg
        self.p_a_1 = 0  # barg
        self.n_h2_out_c = 0  # mol  mass which is set free through the control valve at cathode side
        self.n_o2_out_a = 0  # mol  mass which is set free through the control valve at anode side
        self.pressure_cathode_desire = 20  # barg
        self.pressure_anode_desire = 0  # barg
        self.h2_outflow = 0  # mol/s
        self.o2_outflow = 0  # mol/s
        self.h2o_ouflow_cathode = 0  # mol/s
        self.h2o_outflow_anode = 0  # mol/s
        self.max_h2_outflow = self.calculate_max_hydrogen_outflow(self.electrolyzer_nom_power)

    def calculate(self, time, hydrogen_state: HydrogenState):
        delta_time = time - hydrogen_state.time
        stack_temp = hydrogen_state.temperature_el  #  K
        p_c_0 = hydrogen_state.pressure_cathode_el  # barg
        p_a_0 = hydrogen_state.pressure_anode_el  # barg
        p_h2o_0 = hydrogen_state.sat_pressure_h2o_el  # bar
        n_h2_prod = hydrogen_state.hydrogen_production * delta_time  # mol at stack level
        x_h2o_c = p_h2o_0 / (1 + p_c_0 - p_h2o_0)
        n_o2_prod = hydrogen_state.oxygen_production * delta_time
        x_h2o_a = p_h2o_0 / (1 + p_a_0 - p_h2o_0)
        self.n_h2_out_c = self.__pressure_controller.calculate_n_h2_out(p_c_0, self.pressure_cathode_desire, n_h2_prod, self.max_h2_outflow)
        self.n_o2_out_a = self.__pressure_controller.calculate_n_o2_out(p_a_0, self.pressure_cathode_desire, n_o2_prod)

        # new pressure cathode
        self.p_c_1 = p_c_0 + self.__constants.IDEAL_GAS_CONST * stack_temp / self.VOLUME_GAS_SEPARATOR * (1 + x_h2o_c) * \
                     (n_h2_prod - self.n_h2_out_c ) * 10 ** (-5)  # bar

        # new pressure anode
        self.p_a_1 = p_a_0 + self.__constants.IDEAL_GAS_CONST * stack_temp / self.VOLUME_GAS_SEPARATOR * (1 + x_h2o_a) * \
                     (n_o2_prod - self.n_o2_out_a) * 10 ** (-5)  # bar

        # outflow rates of h2, o2 and h2o
        self.h2_outflow = self.n_h2_out_c / delta_time  # mol/s
        self.o2_outflow = self.n_o2_out_a / delta_time  # mol/s
        self.h2o_ouflow_cathode = x_h2o_c * self.h2_outflow  # mol/s
        self.h2o_outflow_anode = x_h2o_a * self.o2_outflow  # mol/s



    def calculate_max_hydrogen_outflow(self, electrolyzer_nom_power):
        return 0.02 / 5000 * electrolyzer_nom_power  # mol   calculated for timestep of 1 s

    def get_pressure_cathode_el(self) -> float:
        return self.p_c_1

    def get_pressure_anode_el(self) -> float:
        return self.p_a_1

    def get_h2_outflow(self) -> float:
        return self.h2_outflow

    def get_o2_outflow(self) -> float:
        return self.o2_outflow

    def get_h2o_outflow_cathode(self) -> float:
        return self.h2o_ouflow_cathode

    def get_h2o_outflow_anode(self) -> float:
        return self.h2o_outflow_anode
