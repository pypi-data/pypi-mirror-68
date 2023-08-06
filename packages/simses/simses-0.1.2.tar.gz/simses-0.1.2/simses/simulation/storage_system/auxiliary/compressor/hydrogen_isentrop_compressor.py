from simses.simulation.storage_system.auxiliary.compressor.compressor import Compressor
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen


class HydrogenIsentropCompressor(Compressor):
    def __init__(self, compressor_eta):
        super().__init__()
        self.__compressor_eta = compressor_eta
        self.__prefactor = ConstantsHydrogen.HYDROGEN_ISENTROP_EXPONENT / (ConstantsHydrogen.HYDROGEN_ISENTROP_EXPONENT - 1)
        self.__compression_power = 0  # W
        self.__R = ConstantsHydrogen.IDEAL_GAS_CONST
        self.__Z = ConstantsHydrogen.HYDROGEN_REAL_GAS_FACTOR

    def calculate_compression_power(self, hydrogen_flow_out:float, pressure_1: float, pressure_2: float, temperature: float) -> None:
        self.__compression_power = 1 / self.__compressor_eta *self.__prefactor * self.__R * temperature * self.__Z * (( pressure_2 / pressure_1)
                                    ** (1 / self.__prefactor) - 1) * hydrogen_flow_out

    def get_compression_power(self) -> float:
        return self.__compression_power


