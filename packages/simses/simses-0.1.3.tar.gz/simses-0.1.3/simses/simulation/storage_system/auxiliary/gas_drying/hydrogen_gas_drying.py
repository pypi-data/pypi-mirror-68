from simses.simulation.storage_system.auxiliary.gas_drying.gas_drying import GasDrying


class HydrogenGasDrying(GasDrying):

    def __init__(self):
        super().__init__()

        self.__spec_drying_energy = 11.71  #  J/mol h2o
        self.__gas_drying_power = 0  #  W
        self.x_dry = 5 / 1000000  # 5 ppm

    def calculate_gas_drying_power(self, pressure_cathode, h2_outflow, delta_t) -> None:
        x_h2o_after_condens = 0.07981 * pressure_cathode ** (-1.04)  # after condensation at 40°C after curve of: PEM-Elektrolyse-Systeme zur Anwendung in Power-to-Gas Anlagen
        n_h2o_drying = (x_h2o_after_condens - self.x_dry) * h2_outflow * delta_t  # mol
        self.__gas_drying_power = self.__spec_drying_energy * n_h2o_drying  # W

    def get_gas_drying_power(self) -> float:
        return self.__gas_drying_power