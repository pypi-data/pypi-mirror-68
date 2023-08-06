from simses.commons.profile.power_profile.file_power_profile import FilePowerProfile
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.profile_config import ProfileConfig


class LoadProfile(FilePowerProfile):

    def __init__(self, profile_config: ProfileConfig, general_config: GeneralSimulationConfig):
        super().__init__(general_config, profile_config.load_profile,
                         scaling_factor=profile_config.load_scaling_factor)
