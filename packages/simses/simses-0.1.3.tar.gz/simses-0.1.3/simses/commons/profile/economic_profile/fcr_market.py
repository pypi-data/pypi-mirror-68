from simses.commons.log import Logger
from simses.commons.profile.economic_profile.market_profile import MarketProfile
from simses.commons.profile.utils import get_header_from
from simses.config.analysis.market_profile_config import MarketProfileConfig


class FcrMarket(MarketProfile):
    """
    Provides the FCR market prices
    """
    def __init__(self, config: MarketProfileConfig):
        super().__init__()
        self.__config: MarketProfileConfig = config
        self.__file = open(self.__config.fcr_price_file, 'r', newline='')
        self.__header_missing_exception = False
        self.__first_line = None
        self.__header_length = None
        self.__header = get_header_from(self.__config.fcr_price_file)
        self.__log: Logger = Logger(type(self).__name__)

    def next(self) -> float:
        if self.__header_missing_exception is True:
            ffr_data = [x.strip() for x in self.__first_line.split(',')]
            self.__header_missing_exception = False
        else:
            ffr_data = [x.strip() for x in self.__file.readline().split(',')]
        return float(ffr_data[1])

    def read_whole_file_adjusted(self, time_sim_start: float, time_sim_end: float, time_sim_delta: float) -> ([float], [float]):
        # Reads the whole file and adjusts the data if timesteps of price file and simulation vary.
        # The simulation timeframe must be within the market data timeframe.
        time_list = list()
        value_list = list()

        # Check start dates for exceptions
        data1 = [float(x.strip()) for x in self.__file.readline().split(',')]
        time1 = data1[0]
        if time_sim_start < time1:
            self.__log.error('Start date of simulation is smaller than start date of ' + type(self).__name__ +
                             ' Profile. Please align ' + type(self).__name__ +
                             ' Profile and Simulation timeframe.')

        # Move to start time of simulation and check start dates
        while time1 < time_sim_start:
            line = self.__file.readline().split(',')
            if line[0] == '':
                self.__log.error('Start date of simulation is larger than end date of ' + type(self).__name__ +
                                 ' Profile. Please align ' + type(self).__name__ +
                                 ' Profile and Simulation timeframe.')
                break
            data1 = [float(x.strip()) for x in line]
            time1 = data1[0]

        # Determine timestep in price file
        x = self.__file.tell()
        data2 = [float(x.strip()) for x in self.__file.readline().split(',')]
        time_market_delta = data2[0] - time1
        self.__file.seek(x)
        value_list.append(data1[1])
        time_list.append(data1[0])
        time = data1[0]
        del data1, data2

        # Check for other corner cases:
        if time_market_delta < time_sim_delta:
            if time_sim_delta % time_market_delta != 0:
                self.__log.error('Please ensure that simulation timestep is a multiple of '
                                 + type(self).__name__ +' Profile timestep.')
            self.__log.warn('Timesteps for ' + type(self).__name__
                            + 'Profile are smaller than simulation time steps. Averaging market data.')
        elif time_market_delta > time_sim_delta:
            if time_market_delta % time_sim_delta != 0:
                self.__log.error('Please ensure that ' + type(self).__name__
                                 + ' Profile timestep is multiple of simulation timestep.')
            self.__log.warn('Timesteps for ' + type(self).__name__
                            + 'Profile are larger than simulation time steps. Aliasing effects may occur.')

        # Read profile:
        while time <= time_sim_end:
            data = [float(x.strip()) for x in self.__file.readline().split(',')]
            if not data:
                self.__log.error('End date of simulation is after the end date of ' + type(self).__name__ +
                                 ' Profile. Please align ' + type(self).__name__ +
                                 ' Profile and Simulation timeframe.')
            if time_market_delta > time_sim_delta:
                missing_values = int(time_market_delta // time_sim_delta)
                for i in range(missing_values):
                    value_list.append(data[1])
                    time_list.append(time_list[-1] + time_sim_delta)
            if time_market_delta < time_sim_delta:
                missing_values = int(time_sim_delta // time_market_delta)
                avg_list = [data[1]]
                for i in range(missing_values-1):
                    data = [float(x.strip()) for x in self.__file.readline().split(',')]
                    avg_list.append(data[1])
                value_list.append(sum(avg_list) / len(avg_list))
                time_list.append(time_list[-1] + time_sim_delta)
            time = time_list[-1]
        return time_list, value_list

    #def get_header(self) -> dict:
    #    """
    #    Analyzes the header structure and saves it into a dict.
    #    Furthermore sets the __header_length parameter.
    #
    #    Returns
    #    -------
    #    dict
    #        Containing the header parameters and their values.
    #    """
    #    # TODO Please make following code readable
    #    header = {}
    #    line = self.__file.readline()
    #    line_count = 1
    #    if line not in ['"""\r\n']:
    #        self.__header_missing_exception = True
    #        self.__first_line = line
    #        header = None
    #    else:
    #        while line not in ['\r\n']:
    #            if '#' in line:
    #                key_raw, entry_raw = line.split(sep=':')
    #                key = key_raw.strip('# ')
    #                entry = entry_raw.strip()
    #                header[key] = entry
    #            line = self.__file.readline()
    #            line_count += 1
    #        self.__header_length = line_count
    #    return header

    def close(self):
        self.__file.close()



