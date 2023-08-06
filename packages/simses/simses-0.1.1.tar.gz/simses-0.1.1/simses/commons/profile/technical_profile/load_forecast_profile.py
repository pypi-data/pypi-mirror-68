from simses.commons.profile.technical_profile.technical_profile import TechnicalProfile
from simses.commons.profile.utils import get_header_from
from simses.config.simulation.profile_config import ProfileConfig


class LoadForecastProfile(TechnicalProfile):

    def __init__(self, profile_config: ProfileConfig, scaling_factor: float = 1):
        super().__init__()
        self.__file = open(profile_config.load_forecast_file, 'r', newline='')
        self.__header_missing_exception = False
        self.__first_line = None
        self.__header_length = None
        self.__header = get_header_from(profile_config.load_forecast_file)
        self.__scaling_factor = scaling_factor

    def next(self) -> [float]:
        # Handling of profile files with and without header
        if self.__header_missing_exception is True:
            line = self.__first_line
            self.__header_missing_exception = False
        else:
            line = self.__file.readline()
        load_forecast = [float(item) * self.__scaling_factor for item in line.split(',')]
        return load_forecast

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
    #
    #    __header = {}
    #    __line = self.__file.readline()
    #    __line_count = 1
    #    if __line not in ['"""\r\n']:
    #        self.__header_missing_exception = True
    #        self.__first_line = __line
    #        __header = None
    #    else:
    #        while __line not in ['\r\n']:
    #            if '#' in __line:
    #                key_raw, entry_raw = __line.split(sep=':', maxsplit=1)
    #                key = key_raw.strip('# ')
    #                entry = entry_raw.strip()
    #                __header[key] = entry
    #            __line = self.__file.readline()
    #            __line_count += 1
    #        self.__header_length = __line_count
    #    return __header

    def close(self):
        self.__file.close()
