from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion_state import LithiumIonState
from simses.config.data.battery_data_config import BatteryDataConfig
from simses.config.simulation.battery_config import BatteryConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.storage_system_config import StorageSystemConfig
from simses.simulation.storage_system.technology.lithium_ion.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.lithium_ion.cell_type.cell_type import CellType
from simses.simulation.storage_system.technology.lithium_ion.cell_type.dummy_cell import DummyCell
from simses.simulation.storage_system.technology.lithium_ion.cell_type.lfp_sony import SonyLFP
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nca_panasonic_ncr import PanasonicNCA
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_field_data import FieldDataNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_molicel import MolicelNMC
from simses.simulation.storage_system.technology.lithium_ion.cell_type.nmc_sanyo_ur18650e import SanyoNMC
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.cycle_detector import \
    CycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.half_cycle_detector import \
    HalfCycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.cycle_detection.no_cycle_detector import \
    NoCycleDetector
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.degradation_model import DegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.dummy_cell_degradation_model import \
    DummyCellDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.lfp_sony_degradation_model import \
    SonyLFPDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.nca_panasonicNCR_degradation_model import \
    PanasonicNCADegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.nmc_molicel_degradation_model import \
    MolicelNMCDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.nmc_sanyo_ur18650e_degradation_model import \
    SanyoNMCDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.degradation_model.no_degradation_model import \
    NoDegradationModel
from simses.simulation.storage_system.technology.lithium_ion.equivalent_circuit_model.equivalent_circuit_model import \
    EquivalentCircuitModel
from simses.simulation.storage_system.technology.lithium_ion.equivalent_circuit_model.rint_model import RintModel
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.no_thermal_model import NoThermalModel
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.thermal_model import ThermalModel
from simses.simulation.storage_system.technology.lithium_ion.thermal_model.zero_d_thermal_model import ZeroDThermalModel
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel
from simses.simulation.storage_system.thermal_model.system_thermal_model.system_thermal_model import SystemThermalModel


class LithiumIonFactory:
    
    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_factory: StorageSystemConfig = StorageSystemConfig(config)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_battery: BatteryConfig = BatteryConfig(config)
        self.__config_battery_data: BatteryDataConfig = BatteryDataConfig()

    def create_battery_state_from(self, system_id: int, storage_id: int, cell_type: CellType,
                                  ambient_thermal_model: AmbientThermalModel,
                                  battery_state: LithiumIonState = None):
        if battery_state is None:
            time: float = self.__config_general.start
            soc: float = self.__config_battery.soc
            temperature: float = ambient_thermal_model.get_initial_temperature()
            bs = LithiumIonState(system_id, storage_id)
            bs.time = time
            bs.soc = soc
            bs.temperature = temperature
            bs.voltage = cell_type.get_open_circuit_voltage(bs)
            bs.nominal_voltage = cell_type.get_nominal_voltage()
            bs.internal_resistance = cell_type.get_internal_resistance(bs)
            bs.capacity = cell_type.get_capacity() * cell_type.get_nominal_voltage()
            bs.fulfillment = 1.0
            bs.voltage_input = bs.voltage
            return bs
        else:
            return battery_state

    def create_cell_type(self, cell_type: str, voltage: float, capacity: float) -> CellType:
        if cell_type == SonyLFP.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return SonyLFP(voltage, capacity, self.__config_battery_data, self.__config_battery)
        elif cell_type == PanasonicNCA.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return PanasonicNCA(voltage, capacity, self.__config_battery_data, self.__config_battery)
        elif cell_type == MolicelNMC.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return MolicelNMC(voltage, capacity, self.__config_battery_data, self.__config_battery)
        elif cell_type == SanyoNMC.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return SanyoNMC(voltage, capacity, self.__config_battery_data, self.__config_battery)
        elif cell_type == DummyCell.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return DummyCell(voltage, capacity, self.__config_battery)
        elif cell_type == FieldDataNMC.__name__:
            self.__log.debug('Creating cell type as ' + cell_type)
            return FieldDataNMC(voltage, capacity, self.__config_battery)
        else:
            options: [str] = list()
            options.append(SonyLFP.__name__)
            options.append(PanasonicNCA.__name__)
            options.append(MolicelNMC.__name__)
            options.append(SanyoNMC.__name__)
            options.append(DummyCell.__name__)
            options.append(FieldDataNMC.__name__)
            raise Exception('Specified cell type ' + cell_type + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_cycle_detector(self) -> CycleDetector:
        cycle_detector = self.__config_factory.cycle_detector
        if cycle_detector == HalfCycleDetector.__name__:
            self.__log.debug('Creating cycle detector as ' + cycle_detector)
            return HalfCycleDetector(self.__config_battery, self.__config_general)
        elif cycle_detector == NoCycleDetector.__name__:
            self.__log.debug('Creating cycle detector as ' + cycle_detector)
            return NoCycleDetector()
        else:
            self.__log.warn(
                'Specified cycle detector ' + str(cycle_detector) + ' not found, creating ' + NoCycleDetector.__name__)
            return NoCycleDetector()

    def create_degradation_model_from(self, cell_type: CellType,
                                      degradation_model: DegradationModel = None) -> DegradationModel:
        if degradation_model is None:
            cycle_detector: CycleDetector = self.create_cycle_detector()
            if isinstance(cycle_detector, NoCycleDetector):
                self.__log.debug('Creating NoDegradationModel for cell type ' + cell_type.__class__.__name__)
                return NoDegradationModel(cell_type, cycle_detector, self.__config_battery)
            elif isinstance(cell_type, SonyLFP):
                self.__log.debug('Creating degradation model for cell type ' + cell_type.__class__.__name__)
                return SonyLFPDegradationModel(cell_type, cycle_detector, self.__config_battery,
                                               self.__config_general)
            elif isinstance(cell_type, PanasonicNCA):
                self.__log.debug('Creating degradation model for cell type ' + cell_type.__class__.__name__)
                return PanasonicNCADegradationModel(cell_type, cycle_detector, self.__config_battery,
                                                    self.__config_general)
            elif isinstance(cell_type, MolicelNMC):
                self.__log.debug('Creating degradation model for cell type ' + cell_type.__class__.__name__)
                return MolicelNMCDegradationModel(cell_type, cycle_detector, self.__config_battery,
                                                  self.__config_general)
            elif isinstance(cell_type, SanyoNMC):
                self.__log.debug('Creating degradation model for cell type ' + cell_type.__class__.__name__)
                return SanyoNMCDegradationModel(cell_type, cycle_detector, self.__config_battery,
                                                  self.__config_general)
            elif isinstance(cell_type, DummyCell):
                self.__log.debug('Creating degradation model for cell type ' + cell_type.__class__.__name__)
                return DummyCellDegradationModel(cell_type, cycle_detector, self.__config_battery,
                                                 self.__config_general)
            else:
                self.__log.warn('No degradation model found for cell type ' + cell_type.__class__.__name__)
                return NoDegradationModel(cell_type, cycle_detector, self.__config_battery)
        else:
            return degradation_model

    def create_battery_management_system_from(self, cell_type: CellType,
                                              battery_management_system: BatteryManagementSystem = None) -> BatteryManagementSystem:
        if battery_management_system is None:
            self.__log.debug('Creating lithium_ion management system for cell type ' + cell_type.__class__.__name__)
            return BatteryManagementSystem(cell_type, self.__config_battery, self.__config_general)
        else:
            return battery_management_system

    def create_thermal_model_from(self, thermal_model: str, cell_type: CellType,
                                  system_thermal_model: SystemThermalModel) -> ThermalModel:
        if thermal_model == ZeroDThermalModel.__name__:
            self.__log.debug('Creating thermal model for cell type ' + thermal_model.__class__.__name__)
            return ZeroDThermalModel(cell_type, system_thermal_model)
        elif thermal_model == NoThermalModel.__name__:
            self.__log.debug('Creating thermal model for cell type ' + thermal_model.__class__.__name__)
            return NoThermalModel()
        else:
            options: [str] = list()
            options.append(NoThermalModel.__name__)
            options.append(ZeroDThermalModel.__name__)
            raise Exception('Thermal model ' + thermal_model + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_battery_model_from(self, cell_type: CellType,
                                  battery_model: EquivalentCircuitModel = None) -> EquivalentCircuitModel:
        if battery_model is None:
            self.__log.debug('Creating lithium_ion model for cell type ' + cell_type.__class__.__name__)
            return RintModel(cell_type)
        else:
            return battery_model

    def close(self):
        self.__log.close()
