from abc import ABC
from configparser import ConfigParser

from simses.constants_simses import CONFIG_PATH


class Config(ABC):
    """
    The Config class contains all necessary configuration options of a package, e.g. simulation or analysis. In addition,
    the Config class selects proper options from defaults, local or in code configurations.
    """

    __used_config: dict = dict()
    __extensions: [str] = ['.defaults.ini', '.local.ini', '.ini']

    def __init__(self, path: str, name: str, config: ConfigParser):
        if path is None:
            path = CONFIG_PATH
        self.__config: ConfigParser = ConfigParser()
        for extension in self.__extensions:
            self.__config.read(path + name + extension)
            if 'defaults' not in extension or 'local' not in extension:
                self.__file_name: str = name + extension
        self.__overwrite_config_with(config)

    def get_property(self, section: str, option: str):
        """
        Returns the value for given section and option

        Parameters
        ----------
        section :
            section of config
        option :
            option of config

        Returns
        -------

        """
        value = None
        try:
            value = self.__config[section][option]
            self.__add_to_used_config(section, option, value)
        except KeyError as err:
            raise err
        finally:
            return value

    def __overwrite_config_with(self, config: ConfigParser):
        if config is not None:
            for section in config.sections():
                if section in self.__config.sections():
                    for option in config.options(section):
                        if option in self.__config.options(section):
                            value = config[section][option]
                            # print('[' + type(self).__name__ + '] Setting new value in section ' + section +
                            #       ' for option ' + option + ' with ' + value)
                            self.__config[section][option] = value

    def __add_to_used_config(self, section: str, option: str, value: str):
        key: str = self.__file_name
        if key not in self.__used_config.keys():
            self.__used_config[key] = ConfigParser()
        config: ConfigParser = self.__used_config[key]
        if section not in config.sections():
            config.add_section(section)
        if option not in config.options(section):
            config.set(section, option, value)

    def write_config_to(self, path: str) -> None:
        """
        Write current config to a file in given path

        Parameters
        ----------
        path :
            directory in which config file should be written

        Returns
        -------

        """
        # TODO how to write only used configs?
        # used_config: ConfigParser = self.__used_config[self.__file_name]
        with open(path + self.__file_name, 'w') as configfile:
            self.__config.write(configfile)
            # used_config.write(configfile)
