from abc import ABC, abstractmethod
import math

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState


class StackModule(ABC):
    """A StackModule describes a module of connected redox flow stacks"""

    __exact_size: bool = True  # True if serial / parallel connection of stacks can be floats

    def __init__(self, voltage: float, power: float, stack_voltage: float, stack_power: float):
        super().__init__()
        self.__log: Logger = Logger(self.__class__.__name__)
        serial, parallel = self.__stack_connection(voltage, power, stack_voltage, stack_power)
        self._SERIAL_SCALE: float = serial
        self._PARALLEL_SCALE: float = parallel
        self._power_nominal = power
        self.__log.debug('serial: ' + str(serial) + ', parallel: ' + str(parallel))

    def __stack_connection(self, voltage: float, power: float, stack_voltage: float, stack_power: float):
        """
        calculates the number of serial and parallel connected stacks in a stack module to obtain the system voltage and
        power

        Parameters
        ----------
        voltage : float
            voltage of the system
        power : float
            power of the system
        stack_voltage : float
            nominal voltage of one stack
        stack_power : float
            nominal power of one stack

        Returns
        -------
            serial number of stacks connected in one stack module
            parallel number of stacks connected in one stack module

        """
        if self.__exact_size:
            serial: float = voltage / stack_voltage
            parallel: float = power / stack_power * stack_voltage / voltage
            return serial, parallel
        # integer serial and parallel stack numbers, highest number used
        serial: int = math.ceil(voltage / stack_voltage)
        parallel: int = math.ceil(power / stack_power * stack_voltage / voltage)
        return serial, parallel

    @abstractmethod
    def get_open_circuit_voltage(self, ocv_cell: float) -> float:
        """
        Determines the open circuit voltage based on the current RedoxFlowState.

        Parameters
        ----------
        ocv_cell : float
            Current ocv of a single cell of the electrolyte.

        Returns
        -------
        float:
            Open circuit voltage of the stack module in V

        """
        pass

    @abstractmethod
    def get_internal_resistance(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the internal resistance based on the current RedoxFlowState.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of the redox flow battery.

        Returns
        -------
        float:
            Internal resistance of the stack module in Ohm.

        """
        pass

    @abstractmethod
    def get_cell_per_stack(self) -> int:
        """
        Determines the cells per stack for a specific stack type

        Returns
        -------
        int:
            number of cells per stack
        """
        pass

    @abstractmethod
    def get_min_voltage(self) -> float:
        """
        Determines the minimal voltage of a stack module.

        Returns
        -------
        float:
            minimal stack module voltage in V
        """
        pass

    @abstractmethod
    def get_max_voltage(self) -> float:
        """
        Determines the maximal voltage of a stack module.

        Returns
        -------
        float:
            maximal stack module voltage in V
        """
        pass

    @abstractmethod
    def get_min_current(self, redox_flow_state: RedoxFlowState) -> float:
        pass

    @abstractmethod
    def get_max_current(self, redox_flow_state: RedoxFlowState) -> float:
        pass

    @abstractmethod
    def get_self_discharge_current(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Determines the self discharge current, which discharges the stack during standby for a stack module.

        Parameters
        ----------
        redox_flow_state : RedoxFlowState
            Current state of the redox flow battery.

        Returns
        -------
        float:
            self discharge current for a stack module in A
        """
        pass

    @abstractmethod
    def get_stacks_volume(self):
        pass

    @abstractmethod
    def get_nominal_voltage_cell(self) -> float:
        pass

    @abstractmethod
    def get_electrolyte_temperature(self) -> float:
        pass

    def get_name(self) -> str:
        """
        Determines the class name of a stack typ  (e.g. StandardStack)

        Returns
        -------
        str:
            class name of a stack typ
        """
        return self.__class__.__name__

    def get_serial_scale(self) -> float:
        return self._SERIAL_SCALE

    @abstractmethod
    def get_specif_cell_area(self):
        pass

    def get_parallel_scale(self) -> float:
        return self._PARALLEL_SCALE

    def close(self):
        self.__log.close()

    @property
    def power_nominal(self):
        return self._power_nominal
