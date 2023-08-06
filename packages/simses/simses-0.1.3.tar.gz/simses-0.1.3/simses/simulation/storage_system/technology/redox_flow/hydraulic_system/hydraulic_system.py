from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class HydraulicSystem:

    def __init__(self, stack_module: StackModule, pump):
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module = stack_module
        self.__pump = pump
        self.__pressure_drop_anolyte = 10**5
        self.__pressure_drop_catholyte = 10**5
        self.__flow_rate_anolyte = 0.2 * 2160 / 1000000 / 60 * stack_module.get_cell_per_stack() * stack_module._SERIAL_SCALE * stack_module._PARALLEL_SCALE  # m³/s
        self.__flow_rate_catholyte = 0.2 * 2160 / 1000000 / 60 * stack_module.get_cell_per_stack() * stack_module._SERIAL_SCALE * stack_module._PARALLEL_SCALE  # m³/s
        self.__stoichiometry = 10
        self.__FARADAY = 96485  # As/mol
        self.__concentration_vanadium = 1600  # mol/m^3

    def update(self, redox_flow_state: RedoxFlowState):
        redox_flow_state.flow_rate_catholyte = self.get_flow_rate_catholyte(redox_flow_state)
        redox_flow_state.flow_rate_anolyte = self.get_flow_rate_anolyte(redox_flow_state)
        redox_flow_state.pressure_drop_catholyte = self.get_pressure_drop_catholyte(redox_flow_state)
        redox_flow_state.pressure_drop_anolyte = self.get_pressure_drop_anolyte(redox_flow_state)
        redox_flow_state.pressure_loss_catholyte = redox_flow_state.flow_rate_catholyte * redox_flow_state.pressure_drop_catholyte
        redox_flow_state.pressure_loss_anolyte = redox_flow_state.flow_rate_anolyte * redox_flow_state.pressure_drop_anolyte
        power_nominal = self.__stack_module.power_nominal
        # if power is smaller then 5 % of the nominal power, the pumps will not run
        if abs(redox_flow_state.power) < power_nominal * 0.05:
            self.__log.debug('Power is ' + str(redox_flow_state.power) + ' W; pumps will not run.')
            redox_flow_state.pressure_loss_catholyte = 0
            redox_flow_state.pressure_loss_anolyte = 0

        self.__pump.set_eta_pump(redox_flow_state.flow_rate_catholyte)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_catholyte)
        pump_power_catholyte = self.__pump.get_pump_power()
        self.__pump.set_eta_pump(redox_flow_state.flow_rate_anolyte)
        self.__pump.calculate_pump_power(redox_flow_state.pressure_loss_anolyte)
        pump_power_anolyte = self.__pump.get_pump_power()
        redox_flow_state.pump_power = pump_power_catholyte + pump_power_anolyte

    def get_pressure_drop_catholyte(self, redox_flow_state: RedoxFlowState):
        if self.get_flow_rate_catholyte(redox_flow_state) == 0:
            pressure_drop = 0
        else:
            pressure_drop = self.__pressure_drop_catholyte
        return pressure_drop

    def get_pressure_drop_anolyte(self, redox_flow_state: RedoxFlowState):
        if self.get_flow_rate_anolyte(redox_flow_state) == 0:
            pressure_drop = 0
        else:
            pressure_drop = self.__pressure_drop_anolyte
        return pressure_drop

    def get_flow_rate_anolyte(self, redox_flow_state: RedoxFlowState):
        if redox_flow_state.is_charge:
            delta_soc = 1 - redox_flow_state.soc
        else:
            delta_soc = redox_flow_state.soc
        flow_rate = (self.__stoichiometry  * abs(redox_flow_state.current) * self.__stack_module.get_cell_per_stack() *
                     self.__stack_module._SERIAL_SCALE * self.__stack_module._PARALLEL_SCALE/ (self.__FARADAY *
                     self.__concentration_vanadium * delta_soc))
        # if redox_flow_state.power == 0:
        #     flow_rate = 0
        # else:
        #     flow_rate = self.__flow_rate_anolyte
        #
        return flow_rate

    def get_flow_rate_catholyte(self, redox_flow_state: RedoxFlowState):
        if redox_flow_state.is_charge:
            delta_soc = 1 - redox_flow_state.soc
        else:
            delta_soc = redox_flow_state.soc
        flow_rate = (self.__stoichiometry  * abs(redox_flow_state.current) * self.__stack_module.get_cell_per_stack() *
                     self.__stack_module._SERIAL_SCALE * self.__stack_module._PARALLEL_SCALE / (self.__FARADAY *
                     self.__concentration_vanadium * delta_soc))
        # if redox_flow_state.power == 0:
        #     flow_rate = 0
        # else:
        #     flow_rate = self.__flow_rate_catholyte
        # flow_rate = 0.0
        return flow_rate
