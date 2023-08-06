from simses.commons.profile.power_profile.power_profile import PowerProfile


class ConstantPowerProfile(PowerProfile):

    def __init__(self, power: float = 0, scaling_factor: float = 1):
        super().__init__()
        self.__power: float = power
        self.__scaling_factor: float = scaling_factor

    def next(self, time: float) -> float:
        return self.__power * self.__scaling_factor

    def close(self) -> None:
        pass
