from simses.config.simulation.general_config import GeneralSimulationConfig
import pandas as pd
import numpy as np

from simses.config.data.temperature_data_config import TemperatureDataConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class LocationAmbientTemperature(AmbientThermalModel):

    def __init__(self, data_config: TemperatureDataConfig, general_config: GeneralSimulationConfig):
        super().__init__()
        self._filename = data_config.location_file
        self._temperature_data = pd.read_csv(self._filename, delimiter=',', header=None, decimal=".")  # in °C
        # sample_time = 60  # Uncomment for testing
        sample_time = general_config.timestep
        self._start_time = general_config.start
        self._sample_time = general_config.timestep
        self._duration = general_config.duration

        original_temperature = self._temperature_data.to_numpy()
        del self._temperature_data
        original_temperature = original_temperature[0, :]
        original_timesteps = np.arange(1, 8761, 1)
        to_interpolate_time_steps = np.arange(1, 8761, sample_time/3600)
        np.place(to_interpolate_time_steps, to_interpolate_time_steps>8760, 8760)
        interpolated_temperature = np.interp(to_interpolate_time_steps, original_timesteps, original_temperature)

        interpolated_temperature = [273.15 + float(i) for i in interpolated_temperature]
        interpolated_temperature = np.tile(interpolated_temperature,general_config.loop)
        self._temperature = interpolated_temperature

    def get_temperature(self, time) -> float:
        # return self.__temperature
        idx = (int((time - self._start_time)/self._sample_time)-1)
        return self._temperature[idx]

    def get_initial_temperature(self) -> float:
        """
        Returns the ambient temperature

        Parameters
        -------
        time : current simulation time

        Returns
        -------
        float
            ambient temperature in Kelvin
        """
        return self._temperature[0]

    def close(self):
        pass


if __name__ == '__main__':  # Enables isolated debugging and execution of test cases
    print("This only executes when %s is executed rather than imported" % __file__)
    amb = LocationAmbientTemperature()
    temp_1 = amb.get_temperature(10000)

