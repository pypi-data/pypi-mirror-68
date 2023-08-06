from random import Random

from simses.commons.profile.power_profile.power_profile import PowerProfile


class RandomPowerProfile(PowerProfile):

    def __init__(self, start_power=0, max_power=1500, d_power=100, scaling_factor=1):
        super().__init__()
        self.__power = start_power  # W
        self.__d_power = d_power  # W
        self.__max_power = max_power  # W
        self.__random = Random(93823341)
        self.__scaling_factor = scaling_factor

    def next(self, time: float) -> float:
        self.__power += self.__random.uniform(-self.__d_power, self.__d_power)
        self.__power = max(-self.__max_power, min(self.__max_power, self.__power))
        return self.__power * self.__scaling_factor

    def close(self) -> None:
        pass
