from simses.commons.log import Logger
from simses.simulation.storage_system.auxiliary.pump.pump import Pump


class FixEtaCentrifugalPump(Pump):
    """FixEtaCentrifugalPump is a pump with a fixed efficiency"""

    def __init__(self, eta_pump: float):
        super().__init__()
        self.__log: Logger = Logger(type(self).__name__)
        self.__eta_pump = eta_pump
        if self.__eta_pump < 0 or self.__eta_pump > 1:
            self.__log.error('Pump efficiency has to be between 0 and 1.')
        self.__power = 0

    def calculate_pump_power(self, pressure_loss: float) -> None:
        if pressure_loss < 0:
            self.__log.error('Pressure losses are negative.')
        self.__power = pressure_loss / self.__eta_pump

    def set_eta_pump(self, flow_rate):
        pass

    def get_pump_power(self) -> float:
        return self.__power
