from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector


class HalfCycleDetector(CycleDetector):

    def __init__(self, battery_config: BatteryConfig, general_config: GeneralSimulationConfig):
        super().__init__()
        self.__depth_of_cycle = 0
        self.__full_equivalent_cycles = 0
        self.__c_rate = 0
        self.__cycle_step = 1

        self.__last_soc = battery_config.soc
        self.__start_soc = battery_config.soc

        self.__timestep = general_config.timestep
        self.__total_simulation_time = general_config.end

        self.__flag_charging = True
        self.__flag_cycle_detected = False
        self.__flag_constant_soc = True

    def cycle_detected(self, time: float, battery_state: LithiumIonState) -> bool:
        soc = battery_state.soc

        if self.__flag_cycle_detected:
            self._reset_cycle(soc)

        # SOC is constant. First Time = Cycle. Otherwise no cycle detected
        if soc == self.__last_soc and not self.__flag_constant_soc:
            self.__flag_constant_soc = True
            self.__flag_cycle_detected = True
        elif soc == self.__last_soc:
            return False

        # Sign Change check
        if (soc > self.__last_soc and self.__flag_charging) or (soc < self.__last_soc and not self.__flag_charging):
            self._update_cycle_steps(soc)
            self.__flag_constant_soc = False
            self.__flag_cycle_detected = False
        elif (soc < self.__last_soc and self.__flag_charging) or (soc > self.__last_soc and not self.__flag_charging) \
                and self.__cycle_step > 0:
            self.__flag_constant_soc = False
            self.__flag_cycle_detected = True


        # Last simulation step reached
        if battery_state.soc == self.__total_simulation_time:
            self.__flag_cycle_detected = True

        # Update last SOC
        self.__last_soc = soc
        return self.__flag_cycle_detected

    def get_depth_of_full_cycle(self) -> float:
        return self.__depth_of_cycle

    def get_crate(self) -> float:
        return self.__c_rate

    def get_full_equivalent_cycle(self) -> float:
        # add new cycle
        self.__full_equivalent_cycles += self.__depth_of_cycle / 2
        return self.__full_equivalent_cycles

    def reset(self) -> None:
        self.__depth_of_cycle = 0
        self.__full_equivalent_cycles = 0
        self.__cycle_step = 1
        self.__flag_cycle_detected = False

    def _reset_cycle(self, soc) -> None:
        self.__depth_of_cycle = abs(self.__last_soc - soc)
        self.__c_rate = abs(self.__last_soc - soc) / (self.__cycle_step * self.__timestep)
        self.__cycle_step = 1
        self.__start_soc = self.__last_soc
        if soc > self.__last_soc:
            self.__flag_charging = True
        else:
            self.__flag_charging = False


    def _update_cycle_steps(self, soc: float) -> None:
        self.__depth_of_cycle = abs(self.__start_soc - soc)
        self.__c_rate = abs(self.__start_soc - soc) / (self.__cycle_step * self.__timestep)
        self.__cycle_step += 1
        if soc > self.__last_soc:
            self.__flag_charging = True
        else:
            self.__flag_charging = False

    def close(self) -> None:
        pass
