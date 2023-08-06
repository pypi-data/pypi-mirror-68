from datetime import datetime

from pytz import timezone

from simses.commons.log import Logger
from simses.commons.profile.power_profile.power_profile import PowerProfile
from simses.commons.profile.utils import get_header_from
from simses.commons.timeseries.average.average import Average
from simses.commons.timeseries.average.mean_average import MeanAverage
from simses.commons.timeseries.interpolation.interpolation import Interpolation
from simses.commons.timeseries.interpolation.linear_interpolation import LinearInterpolation
from simses.commons.timeseries.timevalue import TimeValue
from simses.config.simulation.general_config import GeneralSimulationConfig


class FilePowerProfile(PowerProfile):

    class Header:
        ANNUAL_CONSUMPTION: str = 'Annual load consumption in kWh'
        DATASET: str = 'Datasets'
        PEAK_POWER: str = 'Nominal power in kWp'
        SAMPLING: str = 'Sampling in s'
        TIMEZONE: str = 'Timezone'
        UNIT: str = 'Unit'

    class Unit:
        WATT: str = 'W'
        KILOWATT: str = 'kW'
        MEGAWATT: str = 'MW'
        GIGAWATT: str = 'GW'

    __TIME_IDX: int = 0
    __VALUE_IDX: int = 1

    __EPOCH_FORMAT: str = 'epoch'
    __DATE_FORMATS: [str] = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', __EPOCH_FORMAT]

    __UTC: timezone = timezone('UTC')
    __BERLIN: timezone = timezone('Europe/Berlin')

    def __init__(self, config: GeneralSimulationConfig, filename: str, delimiter: str = ',', scaling_factor: float = 1):
        super().__init__()
        self.__filename = filename
        self.__log: Logger = Logger(type(self).__name__)
        self.__timestep: float = config.timestep
        self.__start: float = config.start
        self.__end: float = config.end
        self.__time_offset: int = 0
        self.__delimiter: str = delimiter
        self.__scaling_factor: float = scaling_factor
        header: dict = get_header_from(self.__filename)
        self.__unit_factor: float = self.__get_unit_from(header)
        self.__timezone: timezone = self.__get_timezone_from(header)
        self.__interpolation: Interpolation = LinearInterpolation()
        self.__average: Average = MeanAverage()
        self.__last_data: list = list()
        self.__date_format: str = None
        self.__initialize_file()

    def next(self, time: float) -> float:
        data: list = self.__get_data_until(time)
        if self.__interpolation.is_necessary(time, data):
            value = self.__interpolation.interpolate(time, data[-1], data[-2])
        else:
            # TODO clean up code for initial data (mm)
            if len(data) <= 1:
                value = self.__average.average(data)
            elif len(data) <= 2:
                value = self.__average.average(data[1:])
            else:
                value = self.__average.average(data[2:])
        self.__last_data = data[-2:]
        return value * self.__scaling_factor

    def __get_data_until(self, time: float) -> list:
        values: list = list()
        data = self.__last_data[-1]
        while data.time < time:
            data = self.__get_next_data()
            values.append(data)
        values.extend(self.__last_data)
        TimeValue.sort_by_time(values)
        return values

    def __get_next_data(self) -> TimeValue:
        while True:
            line: str = ''
            try:
                line = self.__file.readline()
                if line.startswith('#') or line.startswith('"""') or line in ['\r\n', '\n'] or self.__delimiter not in line:
                    continue
                if line == '':  # end of file_name
                    raise Exception('End of Profile ' + self.__filename + ' reached.')
                data = line.split(self.__delimiter)
                time: float = self.__format_time(data[self.__TIME_IDX]) + self.__time_offset
                value: float = float(data[self.__VALUE_IDX]) * self.__unit_factor
                return TimeValue(time, value)
            except ValueError:
                self.__log.error('No value found for ' + line)

    def __format_time(self, time: str) -> float:
        if self.__date_format is None:
            self.__date_format = self.__find_date_format_for(time)
            self.__log.info('Found format: ' + str(self.__date_format))
        if self.__date_format == self.__EPOCH_FORMAT:
            return float(time)
        else:
            return self.__extract_timestamp_from(time, self.__date_format)

    def __find_date_format_for(self, time: str) -> str:
        for date_format in self.__DATE_FORMATS:
            try:
                if date_format == self.__EPOCH_FORMAT:
                    float(time)
                    return date_format
                else:
                    self.__extract_timestamp_from(time, date_format)
                    return date_format
            except ValueError:
                pass
        raise Exception('Unknown date format for ' + time)

    def __extract_timestamp_from(self, time: str, date_format: str) -> float:
        date: datetime = datetime.strptime(time, date_format)
        date = self.__get_local_datetime_from(date=date)
        return date.timestamp()

    def __get_local_datetime_from(self, date: datetime = None, tstmp: float = None) -> datetime:
        if date is None:
            if tstmp is None:
                tstmp = datetime.now()
            date = datetime.fromtimestamp(tstmp)
        return self.__timezone.localize(date, is_dst=None)

    def __initialize_file(self) -> None:
        self.__file = open(self.__filename, 'r', newline='')
        self.__last_data = self.__get_initial_data()

    def __get_initial_data(self) -> [TimeValue]:
        timestamp: float = self.__start
        data = self.__get_next_data()
        self.__set_time_offset(data.time, timestamp)
        data.time += self.__time_offset
        while data.time < timestamp:
            data = self.__get_next_data()
        return [data]

    def __set_time_offset(self, file_tstmp: float, simulation_tstmp: float) -> None:
        file_date = self.__get_local_datetime_from(tstmp=file_tstmp)
        simulation_date = self.__get_local_datetime_from(tstmp=simulation_tstmp)
        adapted_file_tstmp = file_date.replace(year=simulation_date.year).timestamp()
        self.__time_offset = adapted_file_tstmp - file_tstmp
        if not self.__time_offset == 0:
            self.__log.warn('Time offset is ' + str(self.__time_offset) + ' s. \n'
                            'File time: ' + str(self.__get_local_datetime_from(tstmp=file_tstmp)) + ', \n'
                            'Simulation time: ' + str(self.__get_local_datetime_from(tstmp=simulation_tstmp)))

    def __get_unit_from(self, header: dict) -> float:
        try:
            unit: str = header[self.Header.UNIT]
        except KeyError:
            unit = 'None'
        if unit in self.Unit.WATT:
            return 1
        elif unit in self.Unit.KILOWATT:
            return 1e3
        elif unit in self.Unit.MEGAWATT:
            return 1e6
        elif unit in self.Unit.GIGAWATT:
            return 1e9
        else:
            raise Exception('Not a valid unit in profile ' + self.__filename + '. Valid types are "W","kW","MW","GW".')

    def __get_timezone_from(self, header: dict) -> timezone:
        try:
            tz: str = header[self.Header.TIMEZONE]
            return timezone(tz)
        except KeyError:
            return self.__BERLIN

    def profile_data_to_list(self, sign_factor=1) -> [float]:
        """
        Extracts the whole time series as a list and resets the pointer of the (internal) file afterwards

        Parameters
        ----------
        sign_factor :

        Returns
        -------
        list:
            profile values as a list

        """
        profile_data: [float] = list()
        time = self.__start
        while time <= self.__end - self.__timestep:
            time += self.__timestep
            profile_data.append(self.next(time) * sign_factor)
        self.__initialize_file()
        return profile_data

    def close(self):
        self.__log.close()
        self.__file.close()
