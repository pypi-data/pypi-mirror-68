from simses.commons.data.data_handler import DataHandler
from simses.commons.state.state import State
from simses.commons.state.system_state import SystemState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.control.power_distributor import PowerDistributor
from simses.simulation.storage_system.control.soc_based_power_distributor import SocBasedPowerDistributor
from simses.simulation.storage_system.dc_coupling.dc_coupling import DcCoupling
from simses.simulation.storage_system.housing.housing import Housing
from simses.simulation.storage_system.power_electronics.power_electronics import PowerElectronics
from simses.simulation.storage_system.storage_system_dc import StorageSystemDC
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class StorageSystemAC:
    """AC storage system class"""

    def __init__(self, state: SystemState, data_export: DataHandler, system_thermal_model: SystemThermalModel,
                 power_electronics: PowerElectronics, storage_systems: [StorageSystemDC], dc_couplings: [DcCoupling]
                 , housing: Housing):
        self.__data_export = data_export
        self.__system_state: SystemState = state
        self.__system_id = self.__system_state.get(SystemState.SYSTEM_AC_ID)
        self.__power_electronics: PowerElectronics = power_electronics
        self.__system_thermal_model: SystemThermalModel = system_thermal_model
        self.__storage_systems: [StorageSystemDC] = storage_systems
        self.__dc_couplings: [DcCoupling] = dc_couplings
        self.__auxiliaries: [Auxiliary] = list()
        self.__auxiliaries.extend(self.__system_thermal_model.get_auxiliaries())
        self.__auxiliaries.extend(self.__power_electronics.get_auxiliaries())
        for storage_system in self.__storage_systems:
            self.__auxiliaries.extend(storage_system.get_auxiliaries())
            housing.add_component_volume(storage_system.volume)
        for dc_coupling in self.__dc_couplings:
            self.__auxiliaries.extend(dc_coupling.get_auxiliaries())
        self.__system_state = self.__get_current_state()
        self.__data_export.transfer_data(self.__system_state.to_export())  # initial timestep
        # self.__power_distributor: PowerDistributor = EqualPowerDistributor(len(self.__storage_systems))
        self.__power_distributor: PowerDistributor = SocBasedPowerDistributor()
        housing.add_component_volume(self.__power_electronics.volume)
        self.__system_thermal_model.update_air_parameters()
        self.__housing = housing

    def update(self, power: float, time: float) -> None:
        """
        Function to update the states of an AC storage system

        Parameters
        ----------
        power : ac target power (from energy management system)
        time : current simulation time

        Returns
        -------

        """
        state = self.__system_state
        state.ac_power = power
        # TODO Aux losses are calculated from last timestep. How to implement aux losses for current timestep?
        state.aux_losses = 0
        state.dc_power_additional = 0
        for aux in self.__auxiliaries:
            aux.update(time, state)
        for dc in self.__dc_couplings:
            dc.update(time, state)
        self.__power_electronics.update(time, state)
        self.__system_thermal_model.calculate_temperature(time, state)
        states: [State] = list()
        for system in self.__storage_systems:
            states.append(system.state)
        self.__power_distributor.set(states)
        for system in self.__storage_systems:
            # TODO how to decide whether to store additional dc load or generation? (MM)
            local_power: float = self.__power_distributor.get_power_for(state.dc_power + state.dc_power_additional,
                                                                        system.state)
            system.update(time, local_power)
        for system in self.__storage_systems:
            system.wait()
        state.time = time
        self.__system_state = self.__get_current_state()
        self.__data_export.transfer_data(self.__system_state.to_export())

    def __get_current_state(self) -> SystemState:
        """
        Calculation of current system state

        Returns
        -------
        SystemState:
            Current state of system
        """
        states = list()
        for system in self.__storage_systems:
            states.append(system.state)
        system_state = SystemState.sum_parallel(states)
        system_state.set(SystemState.SYSTEM_AC_ID, self.__system_id)
        system_state.set(SystemState.SYSTEM_DC_ID, 0)
        system_state.time = self.__system_state.time
        system_state.temperature = self.__system_thermal_model.get_temperature()
        system_state.ac_power = self.__system_state.ac_power
        system_state.pe_losses = self.__system_state.pe_losses
        system_state.aux_losses = self.__system_state.aux_losses
        system_state.dc_power_additional = self.__system_state.dc_power_additional
        self.__power_electronics.update_ac_power_from(system_state)
        # Include power electronic fulfillment after reverse power calculation
        system_state.fulfillment *= self.__system_state.fulfillment
        return system_state

    @property
    def state(self) -> SystemState:
        """
        Returns current system state

        Returns
        -------
        SystemState:
            State of the ac system

        """
        return self.__system_state

    def get_housing(self) -> Housing:
        return self.__housing

    def close(self) -> None:
        """
        Closing all open resources in AC storage system

        Parameters
        ----------

        Returns
        -------

        """
        self.__power_electronics.close()
        self.__system_thermal_model.close()
        for storage_system in self.__storage_systems:
            storage_system.close()
        for aux in self.__auxiliaries:
            aux.close()
        for dc_coupling in self.__dc_couplings:
            dc_coupling.close()
