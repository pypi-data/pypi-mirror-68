from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.commons.log import Logger
from simses.config.simulation.redox_flow_config import RedoxFlowConfig
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class BatteryManagementSystem:
    """ BatteryManagementSystem class for redox flow batteries"""

    def __init__(self, stack_module: StackModule, max_power, redox_flow_config: RedoxFlowConfig):
        self.__stack_module: StackModule = stack_module
        self.__max_power = max_power
        self.__log: Logger = Logger(type(self).__name__)
        self.__soc_min = redox_flow_config.min_soc
        self.__soc_max = redox_flow_config.max_soc

    # def check_power_in_range(self, redox_flow_state: RedoxFlowState):
    #     if redox_flow_state.power > self.__max_power:
    #         redox_flow_state.power = self.__max_power


    def check_voltage_in_range(self, redox_flow_state: RedoxFlowState) -> bool:
        """
        checks if voltage is in range between maximal and minimal stack module voltage

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            current state of redox flow battery

        Returns
        -------
        bool:
            true if voltage between max. and min. stack module voltage
        """
        return self.__stack_module.get_min_voltage() <= redox_flow_state.voltage <= self.__stack_module.get_max_voltage()

    def voltage_in_range(self, redox_flow_state: RedoxFlowState) -> float:
        """
        if the voltage is outside of the maximal or minimal stack module voltage, then it is set to the maximal or
        minimal value

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            current state of redox flow battery

        Returns
        -------
        float:
            voltage in V
        """
        voltage_target = redox_flow_state.voltage
        voltage = max(min(voltage_target, self.__stack_module.get_max_voltage()), self.__stack_module.get_min_voltage())
        return voltage

    def check_soc_in_range(self, redox_flow_state: RedoxFlowState, soc: float) -> bool:
        """
        checks if the state-of-charge is to high or to low for charging or discharging

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            current state of redox flow battery

        Returns
        -------
        bool:
            true if SOC is in range for charging or discharging
        """
        if redox_flow_state.is_charge and soc >= self.__soc_max:
            return False
        elif not redox_flow_state.is_charge and soc <= self.__soc_min:
            return False
        else:
            return True

    def check_current_in_range(self, redox_flow_state: RedoxFlowState):
        if redox_flow_state.current > self.__stack_module.get_max_current(redox_flow_state):
            self.__log.error('Flow Rate is to low')
            return False
        elif redox_flow_state.current < self.__stack_module.get_min_current(redox_flow_state):
            self.__log.error('Flow Rate is to low')
            return False
        else:
            return True

    def battery_fulfillment_calc(self, power_target, redox_flow_state: RedoxFlowState):
        power_is = redox_flow_state.power
        if abs(power_is - power_target) < 1e-8:
            redox_flow_state.fulfillment = 1.0
        elif power_target == 0:
            self.__log.error('Power should be 0, but is ' + str(power_is) + ' A. Check BMS function.')
            redox_flow_state.fulfillment = 0.0
        else:
            redox_flow_state.fulfillment = abs(power_is/power_target)
            if redox_flow_state.fulfillment < 0 or redox_flow_state.fulfillment > 1:
                self.__log.error('Fulfillment should be between 0 and 1, but is ' +
                                     str(redox_flow_state.fulfillment) + '. Check BMS functions.')

    def close(self):
        self.__log.close()
