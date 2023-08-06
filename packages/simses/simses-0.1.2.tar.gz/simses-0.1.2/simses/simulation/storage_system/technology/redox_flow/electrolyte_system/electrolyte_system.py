from math import log10

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel


class ElectrolyteSystem:

    def __init__(self, capacity: float, capacity_degradation_model: CapacityDegradationModel):
        self.__log: Logger = Logger(type(self).__name__)
        self.__capacity = capacity
        self.__capacity_degradation_model = capacity_degradation_model
        self.__concentration_v = 1600  # mol/m^3

    def update(self, redox_flow_state: RedoxFlowState):
        self.__capacity = redox_flow_state.capacity
        redox_flow_state.capacity = (self.get_capacity() -
                                     self.__capacity_degradation_model.get_capacity_degradation(redox_flow_state))  # Wh

    def get_capacity(self) -> float:
        """
        Determines the capacity of the redox flow tank system.

        Returns
        -------
        float:
            capacity of the redox flow battery in Wh
        """
        return self.__capacity

    def get_ocv_cell(self, redox_flow_state: RedoxFlowState) -> float:
        """
        Calculates the OCV of a single cell depended on the electrolyte
        Source: Fink, Holger. Untersuchung von Verlustmechanismen in Vanadium-Flussbatterien. Diss. Technische
        Universität München, 2019.
        equation 5.18, assumption: SOH = 100 %, therefore ver = 0.5

        Parameters
        ----------
        temperature : float
            temperature of the electrolyte in K
        redox_flow_state : RedoxFlowState
            current redox_flow_stat

        Returns
        -------
        float:
            ocv of a single cell in V
        """
        soc = redox_flow_state.soc
        temperature = redox_flow_state.electrolyte_temperature
        concentration_h_start = 2.6  # mol/l
        ocv_cell = (1.255 + 0.07 + 0.059 * temperature / 298.15 *
                    log10((soc / (1 - soc) * (concentration_h_start + self.__concentration_v / 1000 * (soc + 0.5)))**2 *
                          (concentration_h_start + self.__concentration_v / 1000 * (soc - 0.5))))
        self.__log.debug('ocv cell: ' + str(ocv_cell))
        return ocv_cell

    def close(self):
        self.__log.close()
