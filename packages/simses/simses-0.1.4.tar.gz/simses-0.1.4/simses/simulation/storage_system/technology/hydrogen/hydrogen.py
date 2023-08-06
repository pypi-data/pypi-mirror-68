from configparser import ConfigParser

from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.simulation.storage_system.auxiliary.auxiliary import Auxiliary
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen
from simses.simulation.storage_system.technology.hydrogen.control.management import HydrogenManagementSystem
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.electrolyzer import Electrolyzer
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.pressure_model_el.pressure_model_el import \
    PressureModelEl
from simses.simulation.storage_system.technology.hydrogen.electrolyzer.thermal_model_el.thermal_model_el import ThermalModelEl
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.fuel_cell import FuelCell
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.pressure_model_fc.pressure_model_fc import \
    PressureModelFc
from simses.simulation.storage_system.technology.hydrogen.fuel_cell.therma_model_fc.thermal_model_fc import \
    ThermalModelFc
from simses.simulation.storage_system.technology.hydrogen.hydrogen_factory import HydrogenFactory
from simses.simulation.storage_system.technology.hydrogen.hydrogen_storage.hydrogen_storage import HydrogenStorage
from simses.simulation.storage_system.technology.technology import StorageTechnology
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class Hydrogen(StorageTechnology):

    MOLAR_MASS_HYDROGEN = 1.00794 * 10 ** (-3) # kg/mol
    FARADAY_CONST: float = 96485.3321  # As/mol
    IDEAL_GAS_CONST: float = 8.314462  # J/(mol K)
    HEAT_CAPACITY_WATER: float = 4184  # J/(kg K)
    MOLAR_MASS_WATER: float = 0.018015  # kg/mol
    HYDROGEN_ISENTROP_EXPONENT = 1.0498  # # from: "Wasserstoff in der Fahrzeugtechnik"
    HYDROGEN_REAL_GAS_FACTOR = 1  # valid for pressures << 13 bar and temperatures >> 33 K


    def __init__(self, data_export: DataHandler, fuel_cell: str, fuel_cell_maximal_power: float, fuel_cell_thermal_model: str, fuel_cell_pressure_model: str, electrolyzer: str,
                 electrolyzer_maximal_power: float, electrolyzer_thermal_model: str, electrolyzer_pressure_model: str, storage: str, capacity: float, max_pressure: float,
                 ambient_thermal_model: AmbientThermalModel, system_thermal_model: SystemThermalModel, system_id: int, storage_id: int, config: ConfigParser):
        super().__init__()
        self.__log = Logger(type(self).__name__)
        self.__data_export: DataHandler = data_export
        self.__factory: HydrogenFactory = HydrogenFactory(config)
        self.__system_thermal_model = system_thermal_model
        self.__ambient_thermal_model = ambient_thermal_model
        self.__management_system: HydrogenManagementSystem = self.__factory.create_hydrogen_management_system(
                                                                electrolyzer_maximal_power, fuel_cell_maximal_power)
        self.__fuel_cell: FuelCell = self.__factory.create_fuel_cell(fuel_cell, fuel_cell_maximal_power)
        self.__electrolyzer: Electrolyzer = self.__factory.create_electrolyzer(electrolyzer, electrolyzer_maximal_power)
        self.constants = ConstantsHydrogen(electrolyzer_maximal_power, self.__electrolyzer.get_nominal_stack_power(),
                                           self.__electrolyzer.get_number_cells(),
                                           self.__electrolyzer.get_geom_area_stack(),
                                           self.__electrolyzer.get_heat_capacity_stack(),
                                           fuel_cell_maximal_power, self.__fuel_cell.get_nominal_stack_power(),
                                           self.__fuel_cell.get_number_cells(),
                                           self.__fuel_cell.get_geom_area_stack(),
                                           self.__fuel_cell.get_heat_capactiy_stack())
        self.__fuel_cell_thermal_model: ThermalModelFc = self.__factory.create_fc_thermal_model(fuel_cell_thermal_model,
                                                        self.__fuel_cell, fuel_cell_maximal_power,
                                                        self.__system_thermal_model, self.__ambient_thermal_model)
        self.__fuel_cell_pressure_model: PressureModelFc = self.__factory.create_fc_pressure_model(fuel_cell_pressure_model)
        self.__electrolyzer_thermal_model: ThermalModelEl = self.__factory.create_el_thermal_model(electrolyzer_thermal_model,
                                                                                                   self.__electrolyzer,
                                                                                                   self.__system_thermal_model, self.__ambient_thermal_model, self.constants)
        self.__electrolyzer_pressure_model: PressureModelEl = self.__factory.create_el_pressure_model(electrolyzer_pressure_model, self.constants)
        self.__hydrogen_storage: HydrogenStorage = self.__factory.create_hydrogen_storage(storage, capacity, max_pressure)
        self.__state: HydrogenState = self.__factory.create_hydrogen_state_from(system_id, storage_id, self.__fuel_cell,
                                                                                self.__electrolyzer,
                                                                                storage=self.__hydrogen_storage,
                                                                                ambient_thermal_model=self.__ambient_thermal_model,
                                                                                hydrogen_storage=self.__hydrogen_storage)
        self.electrolyzer_auxiliaries = self.__electrolyzer.get_auxiliaries_electrolyzer()
        self.fuel_cell_auxiliaries = self.__fuel_cell.get_auxiliaries_fuel_cell()



    def distribute_and_run(self, time: float, current: float, voltage: float):
        hs: HydrogenState = self.__state
        hs.power = current * voltage
        self.__management_system.update(time, hs)
        if self.__state.is_charge:
            power_electrolyzer = hs.power
            power_fuel_cell = 0
        else:
            power_electrolyzer = 0
            power_fuel_cell = hs.power
        self.__electrolyzer.update(time, hs, power_electrolyzer, self.__electrolyzer_pressure_model, self.__electrolyzer_thermal_model)
        self.__fuel_cell.update(time, hs, power_fuel_cell, self.__fuel_cell_pressure_model, self.__fuel_cell_thermal_model)
        hs.voltage = 1
        hs.convection_heat = self.__electrolyzer.get_convection_heat_el()
        self.__hydrogen_storage.update(time, hs)
        timestep = time - hs.time
        hs.time = time
        self.__data_export.transfer_data(hs.to_export())
        self.__log.info('Done with update')

    @property
    def volume(self) -> float:
        return 0

    def wait(self):
        pass

    def get_auxiliaries(self) -> [Auxiliary]:
        return self.electrolyzer_auxiliaries + self.fuel_cell_auxiliaries
        #return list()

    @property
    def state(self):
        return self.__state

    def close(self):
        self.__factory.close()
        self.__management_system.close()
        self.__log.close()
