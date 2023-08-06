from configparser import ConfigParser

from simses.config.config import Config


class SimulationConfig(Config):

    config_name: str = 'simulation'

    def __init__(self, path: str, config: ConfigParser):
        super().__init__(path, self.config_name, config)


def create_dict_from(properties: [str]) -> dict:
    res: dict = dict()
    for prop in properties:
        items: list = prop.split(',')
        name: str = items.pop(0)
        if name in res.keys():
            raise Exception(name + ' is not unique. Please check your config file.')
        res[name] = items
    return res


def create_list_from(properties: [str]) -> [[str]]:
    res: [[str]] = list()
    for prop in properties:
        res.append(prop.split(','))
    return res


def clean_split(properties: str) -> [str]:
    props: [str] = properties.replace(' ', '').replace('\t', '').split('\n')
    copy = props[:]
    for prop in copy:
        if not prop:
            props.remove(prop)
    return props
