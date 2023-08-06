
class TimeValue:

    def __init__(self, tstmp: float, value: float):
        self.__tstmp: float = tstmp
        self.__value: float = value

    @property
    def time(self) -> float:
        return self.__tstmp

    @time.setter
    def time(self, value: float) -> None:
        self.__tstmp = value

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float) -> None:
        self.__value = value

    def __str__(self) -> str:
        return '\n(' + str(self.time) + ', ' + str(self.value) + ')'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def sort_by_time(data: list):
        data.sort(key=lambda x: x.time, reverse=False)
