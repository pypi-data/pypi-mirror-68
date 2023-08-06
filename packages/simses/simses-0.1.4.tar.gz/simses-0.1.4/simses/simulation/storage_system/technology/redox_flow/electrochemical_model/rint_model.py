from math import sqrt

from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.commons.log import Logger
from simses.simulation.storage_system.technology.redox_flow.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.electrochemical_model import \
    ElectrochemicalModel
from simses.simulation.storage_system.technology.redox_flow.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule


class RintModel(ElectrochemicalModel):

    def __init__(self, stack_module: StackModule, battery_management_system: BatteryManagementSystem,
                 electrolyte_system: ElectrolyteSystem):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__stack_module: StackModule = stack_module
        self.__battery_management_system: BatteryManagementSystem = battery_management_system
        self.__electrolyte_system: ElectrolyteSystem = electrolyte_system
        self.__FARADAY = 96485  # As/mol
        self.__concentration_V = 1600  # mol/m³

    def update(self, time: float, redox_flow_state: RedoxFlowState, power_target) -> None:

        stack_module: StackModule = self.__stack_module
        bms: BatteryManagementSystem = self.__battery_management_system
        electrolyte_system: ElectrolyteSystem = self.__electrolyte_system
        rfbs: RedoxFlowState = redox_flow_state
        temperature = stack_module.get_electrolyte_temperature()
        ocv_cell: float = electrolyte_system.get_ocv_cell(rfbs)
        ocv: float = stack_module.get_open_circuit_voltage(ocv_cell)  # V
        rint: float = stack_module.get_internal_resistance(rfbs)

        # bms.check_power_in_range(rfbs)

        rfbs.voltage = (ocv + sqrt(ocv**2 + 4 * rint * rfbs.power))/2
        self.__log.debug('OCV System: ' + str(ocv))
        self.__log.debug('Voltage: ' + str(rfbs.voltage))

        # voltage check
        if not bms.check_voltage_in_range(rfbs):
            self.__log.warn('Voltage is not in range ' + str(rfbs.voltage) + ' but adjusted to value in range.')
            rfbs.voltage = bms.voltage_in_range(rfbs)
        self.__log.debug('Voltage after BMS: ' + str(rfbs.voltage))

        rfbs.current = rfbs.power/rfbs.voltage

        # current check
        if not bms.check_current_in_range(rfbs):
            self.__log.warn('Current is not in range' + str(rfbs.current) + 'Max ' + str(stack_module.get_max_current(rfbs)) + 'Min ' + str(stack_module.get_min_current(rfbs)))

            if redox_flow_state.current > 0:
                rfbs.current = stack_module.get_max_current(rfbs)
            else:
                rfbs.current = stack_module.get_min_current(rfbs)
            rfbs.voltage = rfbs.current * rint + ocv

        soc, soc_stack = self.__calculate_soc(time, rfbs, stack_module)

        # SOC check
        if not bms.check_soc_in_range(rfbs, soc):
            self.__log.warn('RFB should not be charged/discharged due to SOC restrictions. SOC: ' + str(rfbs.soc) + ', power (' + str(rfbs.power) + ') is set to 0')
            rfbs.current = 0.0
            rfbs.voltage = ocv
            soc, soc_stack = self.__calculate_soc(time, rfbs, stack_module)

        rfbs.power = rfbs.current * rfbs.voltage
        rfbs.power_loss = rint * rfbs.current ** 2
        rfbs.soc_stack = soc_stack
        rfbs.soc = soc
        rfbs.electrolyte_temperature = temperature
        self.__log.debug('New SOC: ' + str(soc))

        # check SOC > 0
        if rfbs.soc < 0.0:
            self.__log.warn('SOC was tried to be set to a value of ' + str(rfbs.soc) + ' but adjusted to 0.')
            rfbs.soc = max(rfbs.soc, 0.0)
        elif rfbs.soc < 1e-7:
            self.__log.warn('SOC was tried to be set to a value of ' + str(rfbs.soc) + ' but adjusted to 0.')
            rfbs.soc = 0.0

        # battery fulfillment
        bms.battery_fulfillment_calc(power_target, rfbs)

        rfbs.internal_resistance = rint
        rfbs.open_circuit_voltage = ocv

    def __calculate_soc(self, time: float, rfbs: RedoxFlowState, stack_module: StackModule):
        """
        calculates the soc of the system and in the cell

        Parameters
        ----------
        time : float
            current simulation time in s
        rfbs : RedoxFlowState
            current redox flow battery state
        stack_module : StackModule
            type of redox flow battery stack module

        Returns
        -------
            soc in p.u.
            soc_stack in p.u.
        """
        cell_num_stack = stack_module.get_cell_per_stack()
        self_discharge_current: float = stack_module.get_self_discharge_current(rfbs)
        soc_stack = rfbs.soc_stack
        capacity_amps = rfbs.capacity * 3600 / stack_module.get_nominal_voltage_cell()  # As

        if rfbs.current == 0:
            # self_discharge_current = 0   # for no self-discharge during standby
            soc_stack -= self_discharge_current * (time-rfbs.time) / (self.__FARADAY * self.__concentration_V * stack_module.get_stacks_volume())
            if soc_stack < 0:
                self.__log.warn('Stack is totally discharged.')
                soc_stack = 0
                self_discharge_current = 0

        soc = rfbs.soc + (rfbs.current * cell_num_stack * stack_module.get_serial_scale() - self_discharge_current) * (time - rfbs.time) / capacity_amps
        self.__log.debug('New calculated SOC: ' + str(soc))
        self.__log.debug('delta t: ' + str(time - rfbs.time))
        self.__log.debug('capacity_amps: ' + str(capacity_amps))
        if not rfbs.current == 0:
            soc_stack = soc
        self.__log.debug('Current: ' + str(rfbs.current) + ' , self-discharge-Current: ' + str(self_discharge_current))
        return soc, soc_stack

    def close(self) -> None:
        self.__log.close()
        self.__stack_module.close()
        self.__battery_management_system.close()
