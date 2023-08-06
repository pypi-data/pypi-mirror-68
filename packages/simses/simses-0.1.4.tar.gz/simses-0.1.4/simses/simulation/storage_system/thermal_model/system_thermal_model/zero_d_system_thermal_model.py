from simses.commons.state.system_state import SystemState
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.auxiliary.heating_ventilation_air_conditioning.hvac import \
    HeatingVentilationAirConditioning
from simses.simulation.storage_system.housing.housing import Housing
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class ZeroDSystemThermalModel(SystemThermalModel):
    """This model functions at Storage System Level.
    System Air Temperature is computed here.
    Energy Balance around System Air is applied."""

    def __init__(self, ambient_thermal_model: AmbientThermalModel, housing: Housing, hvac: HeatingVentilationAirConditioning, general_config: GeneralSimulationConfig):
        super().__init__()
        self.start_time: float = general_config.start
        self.__ambient_thermal_model: AmbientThermalModel = ambient_thermal_model
        self.__system_temperature: float = self.__ambient_thermal_model.get_initial_temperature()  # K
        self.sample_time: float = general_config.timestep
        # this is the internal air temperature within the container. Initialized with ambient temperature
        self.__housing: Housing = housing  # Link housing object to thermal model definition
        self.__heating_cooling: HeatingVentilationAirConditioning = hvac
        self.__air_conditioning_heat: float = 0
        self.__set_point_temperature: float = self.__heating_cooling.get_set_point_temperature()  # K

        # Air parameters
        self.__individual_gas_constant = self.universal_gas_constant / self.molecular_weight_air  # J/kgK
        self.__air_density = self.air_pressure / (self.__individual_gas_constant * self.__system_temperature)  # kg/m3
        # TODO link volumes of ac systems within housing
        # TODO System Air volume = 80% container volume is a temporary measure.
        self.update_air_parameters()
        self.__air_specific_heat = 1006  # J/kgK, cp (at constant pressure)
        # Model with p & V constant, i.e. if T rises, mass must decrease.
        # Quantities with reference to ideal gas equation

    def update_air_parameters(self):
        self.__air_volume = self.__housing.internal_air_volume  # - sum of volumes of AC systems within (rating * volumetric energy/power density)
        self.__air_mass = self.__air_volume * self.__air_density  # kg

    def calculate_temperature(self, time, state: SystemState) -> None:
        net_thermal_resistance = (1 / self.__housing.internal_surface_area * (
                1 / self.__housing.convection_coefficient_air_L1 + self.__housing.thickness_L1 / self.__housing.thermal_conductivity_L1 + self.__housing.thickness_L2 / self.__housing.thermal_conductivity_L2) + 1 / self.__housing.external_area * (
                                          self.__housing.thickness_L3 / self.__housing.thermal_conductivity_L3 + 1 / self.__housing.convection_coefficient_L3_air))
        temperature_gradient = self.__system_temperature - self.__ambient_thermal_model.get_temperature(time)
        conduction_heat = -temperature_gradient / net_thermal_resistance  # W
        # conduction heat is -ve when system air is hotter than ambient air,
        # convection heat is -ve when battery is hotter than system air

        self.__air_density = self.air_pressure / (self.__individual_gas_constant * self.__system_temperature)  # kg/m3
        delta_t_air = self.sample_time * (-state.convection_heat + conduction_heat) / (
                    self.__air_mass * self.__air_specific_heat)  # K
        air_temperature = delta_t_air + self.__system_temperature  # K

        air_conditioning_thermal_power_required = (self.__air_mass * self.__air_specific_heat) * (
                    self.__set_point_temperature - air_temperature) / self.sample_time  # W
        # air conditioning thermal power required is +ve when heating takes place
        self.__heating_cooling.run_air_conditioning(air_conditioning_thermal_power_required)
        air_conditioning_thermal_power_actual = self.__heating_cooling.get_thermal_power()  # W

        delta_t_air_heating_cooling = self.sample_time * air_conditioning_thermal_power_actual / (
                    self.__air_mass * self.__air_specific_heat)  # K
        self.__system_temperature = air_temperature + delta_t_air_heating_cooling

    def get_auxiliaries(self) -> [Auxiliary]:
        return [self.__heating_cooling]

    def get_temperature(self) -> float:
        return self.__system_temperature

    def get_air_mass(self) -> float:
        return self.__air_mass

    def get_air_specific_heat(self) -> float:
        return self.__air_specific_heat

    def close(self):
        self.__housing.close()
