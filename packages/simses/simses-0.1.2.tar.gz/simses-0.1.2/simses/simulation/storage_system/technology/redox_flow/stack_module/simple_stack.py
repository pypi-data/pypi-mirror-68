

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class SimpleStack(StackModule):

    __CELL_VOLTAGE_NOM = 1.4  # V
    __CELL_NUMBER = 20  # -
    __INTERNAL_RESISTANCE = 1  # Ohmcm^2
    __CELL_AREA = 1000  # cm^2
    __CELL_THICKNESS = 0.37  # cm
    __ELECTRODE_POROSITY = 0.9  # -
    __MIN_CELL_VOLTAGE = 1.0  # V
    __MAX_CELL_VOLTAGE = 1.6  # V
    __SELF_DISCHARGE_CURRENT_DENS = 1  # mA/cm²
    __STACK_VOLTAGE_NOM = __CELL_VOLTAGE_NOM * __CELL_NUMBER  # V
    __STACK_POWER_NOM = 3164  # W

    def __init__(self, voltage: float, power: float):
        super().__init__(voltage, power, self.__STACK_VOLTAGE_NOM, self.__STACK_POWER_NOM)
        self.__log: Logger = Logger(__name__)
        self.__FARADAY = 96485  # As/mol
        self.__concentration_v = 1600  # mol/m³
        self.__temperature = 303.15  # K
        self.__flow_rate = 0.4 * self.__CELL_AREA / 1000000 / 60 * self.__CELL_NUMBER * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m³/s

    def get_open_circuit_voltage(self, ocv_cell) -> float:
        return ocv_cell * self.__CELL_NUMBER * self._SERIAL_SCALE

    def get_internal_resistance(self, redox_flow_state: RedoxFlowState) -> float:
        resistance = self.__INTERNAL_RESISTANCE / self.__CELL_AREA
        return float(resistance * self.__CELL_NUMBER * self._SERIAL_SCALE / self._PARALLEL_SCALE)

    def get_cell_per_stack(self) -> int:
        return self.__CELL_NUMBER

    def get_min_voltage(self) -> float:
        return self.__MIN_CELL_VOLTAGE * self.__CELL_NUMBER * self._SERIAL_SCALE

    def get_max_voltage(self) -> float:
        return self.__MAX_CELL_VOLTAGE * self.__CELL_NUMBER * self._SERIAL_SCALE

    def get_min_current(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        min_current = (-soc * self.__FARADAY * self.__concentration_v * self.__flow_rate / self._SERIAL_SCALE
                       / self.__CELL_NUMBER)
        self.__log.debug('Min Current: ' + str(min_current))
        return min_current

    def get_max_current(self, redox_flow_state: RedoxFlowState) -> float:
        soc = redox_flow_state.soc
        max_current = ((1 - soc) * self.__FARADAY * self.__concentration_v * self.__flow_rate / self._SERIAL_SCALE
                       / self.__CELL_NUMBER)
        self.__log.debug('Max Current: ' + str(max_current))
        return max_current

    def get_self_discharge_current(self, redox_flow_state: RedoxFlowState) -> float:
        return (self.__SELF_DISCHARGE_CURRENT_DENS * self.__CELL_AREA * self.__CELL_NUMBER * self._SERIAL_SCALE
                * self._PARALLEL_SCALE / 1000)

    def get_stacks_volume(self):
        return (self.__CELL_AREA * self.__CELL_THICKNESS * self.__CELL_NUMBER * self._SERIAL_SCALE
                * self._PARALLEL_SCALE * self.__ELECTRODE_POROSITY / 1000000)  # m^3

    def get_nominal_voltage_cell(self) -> float:
        return self.__CELL_VOLTAGE_NOM

    def get_electrolyte_temperature(self) -> float:
        return self.__temperature

    def get_specif_cell_area(self):
        return self.__CELL_AREA
