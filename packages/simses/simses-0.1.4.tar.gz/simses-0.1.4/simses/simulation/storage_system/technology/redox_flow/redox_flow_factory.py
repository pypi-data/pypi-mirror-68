from configparser import ConfigParser

from simses.commons.log import Logger
from simses.commons.state.technology.redox_flow_state import RedoxFlowState
from simses.config.data.auxiliary_data_config import AuxiliaryDataConfig
from simses.config.data.redox_flow_data_config import RedoxFlowDataConfig
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.config.simulation.redox_flow_config import RedoxFlowConfig
from simses.simulation.storage_system.auxiliary.pump.fixeta_centrifugal_pump import FixEtaCentrifugalPump
from simses.simulation.storage_system.auxiliary.pump.pump import Pump
from simses.simulation.storage_system.auxiliary.pump.variable_eta_centrifugal_pump import VariableEtaCentrifugalPump
from simses.simulation.storage_system.technology.redox_flow.battery_management_system.battery_management_system import \
    BatteryManagementSystem
from simses.simulation.storage_system.technology.redox_flow.degradation_model.capacity_degradation_model import \
    CapacityDegradationModel
from simses.simulation.storage_system.technology.redox_flow.degradation_model.const_hydrogen_current import \
    ConstHydrogenCurrent
from simses.simulation.storage_system.technology.redox_flow.degradation_model.no_degradation_model import NoDegradation
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.electrochemical_model import \
    ElectrochemicalModel
from simses.simulation.storage_system.technology.redox_flow.electrochemical_model.rint_model import RintModel
from simses.simulation.storage_system.technology.redox_flow.electrolyte_system.electrolyte_system import \
    ElectrolyteSystem
from simses.simulation.storage_system.technology.redox_flow.hydraulic_system.hydraulic_system import HydraulicSystem
from simses.simulation.storage_system.technology.redox_flow.stack_module.simple_stack import SimpleStack
from simses.simulation.storage_system.technology.redox_flow.stack_module.stack_module import StackModule
from simses.simulation.storage_system.technology.redox_flow.stack_module.standard_stacks import StandardStack
from simses.simulation.storage_system.thermal_model.ambient_thermal_model.ambient_thermal_model import \
    AmbientThermalModel


class RedoxFlowFactory:

    def __init__(self, config: ConfigParser):
        self.__log: Logger = Logger(type(self).__name__)
        self.__config_general: GeneralSimulationConfig = GeneralSimulationConfig(config)
        self.__config_redox_flow: RedoxFlowConfig = RedoxFlowConfig(config)
        self.__config_redox_flow_data: RedoxFlowDataConfig = RedoxFlowDataConfig()
        self.__config_auxiliary_data: AuxiliaryDataConfig = AuxiliaryDataConfig()

    def create_redox_flow_state_from(self, storage_id: int, system_id: int, ambient_thermal_model: AmbientThermalModel,
                                     stack_module: StackModule, electrolyte_system: ElectrolyteSystem,
                                     redox_flow_state: RedoxFlowState = None):
        """
        Initial creates the RedoxFlowState object if it does't exist.

        Parameters
        ----------
        storage_id : int
            storage id
        system_id : int
            system id
        ambient_thermal_model: AmbientThermalModel
            AmbientThermalModel to get initial temperature
        stack_module : StackModule
            stack module based on specific stack typ
        electrolyte_system : ElectrolyteSystem
            electrolyte system of the redox flow battery
        redox_flow_state : RedoxFlowState

        Returns
        -------
        RedoxFlowState
            state of the redox flow battery
        """
        if redox_flow_state is None:
            time: float = self.__config_general.start
            soc: float = self.__config_redox_flow.soc
            rfbs = RedoxFlowState(system_id, storage_id)
            rfbs.time = time
            rfbs.soc = soc
            rfbs.soc_stack = soc
            rfbs.voltage = stack_module.get_open_circuit_voltage(1.4)
            rfbs.open_circuit_voltage = stack_module.get_open_circuit_voltage(1.4)
            rfbs.capacity = electrolyte_system.get_capacity()
            rfbs.internal_resistance = stack_module.get_internal_resistance(rfbs)
            rfbs.power = 0.0
            rfbs.power_loss = 0.0
            rfbs.pressure_loss = 0.0
            rfbs.pressure_drop_anolyte = 0.0
            rfbs.pressure_drop_catholyte = 0.0
            rfbs.flow_rate_anolyte = 0.0
            rfbs.flow_rate_catholyte = 0.0
            rfbs.fulfillment = 1.0
            rfbs.electrolyte_temperature = 303.15
            return rfbs
        else:
            return redox_flow_state

    def create_stack_module(self, stack_module: str, voltage: float, power: float) -> StackModule:
        """
        Initial creates the StackModule object for a specific stack typ.

        Parameters
        ----------
        stack_module : str
            stack type for stack module
        voltage : float
            nominal stack module voltage in V of the redox flow battery
        power : float
            nominal stack module power in W of the redox flow battery

        Returns
        -------
        StackModule
        """
        if stack_module == StandardStack.__name__:
            self.__log.debug('Creating stack module as ' + stack_module)
            return StandardStack(voltage, power, self.__config_redox_flow_data)
        elif stack_module == SimpleStack.__name__:
            self.__log.debug('Creating stack module as ' + stack_module)
            return SimpleStack(voltage, power)
        else:
            options: [str] = list()
            options.append(StandardStack.__name__)
            options.append(SimpleStack.__name__)
            raise Exception('Specified stack module ' + stack_module + ' is unknown. '
                            'Following options are available: ' + str(options))

    def create_pumps(self, eta_pump, pump_type: str):
        if pump_type == FixEtaCentrifugalPump.__name__:
            self.__log.debug('Crating pumps as ' + pump_type)
            return FixEtaCentrifugalPump(eta_pump)
        elif pump_type == VariableEtaCentrifugalPump.__name__:
            self.__log.debug('Crating pumps as ' + pump_type)
            return VariableEtaCentrifugalPump(self.__config_auxiliary_data)
        else:
            options: [str] = list()
            options.append(FixEtaCentrifugalPump.__name__)
            raise Exception('Specified pump type ' + pump_type + ' is unknown.'
                            'Following options are available: ' + str(options))

    def create_hydraulic_system(self, stack_module: StackModule, pump, hydraulic_system: HydraulicSystem = None):
        """
        Initial creates the HydraulicSystem object.
        Parameters
        ----------
        stack_module : StackModule
        pump: Pump
        hydraulic_system : HydraulicSystem

        Returns
        -------
        HydraulicSystem
        """
        if hydraulic_system is None:
            self.__log.debug('Creating hydraulic system for redox flow system ')
            return HydraulicSystem(stack_module, pump)
        else:
            return hydraulic_system

    def create_electrolyte_system(self, capacity: float, capacity_degradation_model: CapacityDegradationModel,
                                  electrolyte_system: ElectrolyteSystem = None) -> ElectrolyteSystem:
        """
        Initial creates the ElectrolyteSystem object.

        Parameters
        ----------
        capacity : float
            electrolyte system capacity in Wh of the redox flow battery
        electrolyte_system : ElectrolyteSystem

        Returns
        -------
        ElectrolyteSystem
        """
        if electrolyte_system is None:
            self.__log.debug('Creating electrolyte system for redox flow system ')
            return ElectrolyteSystem(capacity, capacity_degradation_model)
        else:
            return electrolyte_system

    def create_electrochemical_model(self, stack_module: StackModule, battery_management_system: BatteryManagementSystem
                                     , electrolyte_system: ElectrolyteSystem
                                     , electrochemical_model: ElectrochemicalModel = None) -> ElectrochemicalModel:
        """
        Initial creates the ElectrochemicalModel object for a specific model, which includes the battery management system requests.

        Parameters
        ----------
        stack_module : StackModule
            stack module of a redox flow battery
        battery_management_system : BatteryManagementSystem
            battery management system of the redox flow battery
        electrolyte_system: ElectrolyteSystem
            electrolyte system of the redox flow battery
        electrochemical_model : ElectrochemicalModel
            electrochemical model of the redox flow battery

        Returns
        -------
            ElectrochemicalModel
        """
        if electrochemical_model is None:
            self.__log.debug('Creating electrochemical model for redox flow system depended on stack module ' +
                             stack_module.__class__.__name__)
            return RintModel(stack_module, battery_management_system, electrolyte_system)
        else:
            return electrochemical_model

    def create_battery_management_system(self, stack_module: StackModule,
                                         max_power,
                                         battery_management_system: BatteryManagementSystem = None) \
            -> BatteryManagementSystem:
        """
        Initial creates the BatteryManagementSystem object of the redox flow battery.

        Parameters
        ----------
        stack_module : StackModule
             stack module of a redox flow battery
        battery_management_system : BatteryManagementSystem
            battery management system of the redox flow battery

        Returns
        -------
            BatteryManagementSystem
        """
        if battery_management_system is None:
            self.__log.debug('Creating battery management system for redox flow system depended on stack module '
                             + stack_module.__class__.__name__)
            return BatteryManagementSystem(stack_module, max_power, self.__config_redox_flow)
        else:
            return battery_management_system

    def create_degradation_model(self, stack_module: StackModule, general_config: GeneralSimulationConfig,
                                 degradation_model: str):
        if degradation_model == NoDegradation.__name__:
            self.__log.debug('Creating degradation Model as ' + degradation_model)
            return NoDegradation()
        elif degradation_model == ConstHydrogenCurrent.__name__:
            self.__log.debug('Creating degradation Model as ' + degradation_model)
            return ConstHydrogenCurrent(stack_module, general_config)
        else:
            options: [str] = list()
            options.append(NoDegradation.__name__)
            options.append(ConstHydrogenCurrent.__name__)
            raise Exception('Specified stack module ' + degradation_model + ' is unknown. '
                                                                       'Following options are available: ' + str(
                options))

    def close(self):
        self.__log.close()
