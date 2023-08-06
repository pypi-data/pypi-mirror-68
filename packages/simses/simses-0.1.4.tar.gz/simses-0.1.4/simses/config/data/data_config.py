from simses.config.config import Config


class DataConfig(Config):

    config_name: str = 'data'

    def __init__(self, path: str):
        super().__init__(path, self.config_name, None)
