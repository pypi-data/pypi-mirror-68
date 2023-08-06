from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.analysis.utils import get_max_for
from simses.commons.state.energy_management_state import EnergyManagementState
from simses.commons.state.system_state import SystemState
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig
from simses.config.simulation.energy_management_config import EnergyManagementConfig


class SiteLevelEvaluation(TechnicalEvaluation):

    title = 'Site Level Power'

    def __init__(self, data: SystemData, energy_management_data: EnergyManagementData, config: GeneralAnalysisConfig,
                 energy_management_config: EnergyManagementConfig, path: str):
        super().__init__(energy_management_data, config)
        self.__system_data: SystemData = data
        self.__ems_config: EnergyManagementConfig = energy_management_config
        self.__max_power: float = energy_management_config.max_power
        title_extension: str = ' for system ' + self.get_data().id
        self.title += title_extension
        self.__result_path = path

    def evaluate(self):
        power_above_peak = self.power_above_peak
        energy_events_above_peak = self.energy_events_above_peak(power_above_peak)
        self.append_result(EvaluationResult(Description.Technical.POWER_ABOVE_PEAK_MAX, Unit.WATT, self.max_power_above_peak(power_above_peak)))
        self.append_result(EvaluationResult(Description.Technical.POWER_ABOVE_PEAK_AVG, Unit.WATT, self.get_average_power_above_peak_from(power_above_peak)))
        self.append_result(EvaluationResult(Description.Technical.ENERGY_ABOVE_PEAK_MAX, Unit.KWH, self.get_max_energy_event_above_peak_from(energy_events_above_peak)))
        self.append_result(EvaluationResult(Description.Technical.ENERGY_ABOVE_PEAK_AVG, Unit.KWH, self.get_average_energy_event_above_peak_from(energy_events_above_peak)))
        self.append_result(EvaluationResult(Description.Technical.NUMBER_ENERGY_EVENTS, Unit.NONE, len(energy_events_above_peak)))
        self.print_results()

    def plot(self) -> None:
        ems_data: EnergyManagementData = self.get_data()
        system_data: SystemData = self.__system_data
        plot: Plotting = PlotlyPlotting(title=self.title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(system_data.time), label=SystemState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(system_data.power, label=SystemState.AC_POWER_DELIVERED, color=PlotlyPlotting.Color.BLACK,
                          linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(ems_data.load_power, label=EnergyManagementState.LOAD_POWER,
                          color=PlotlyPlotting.Color.GREEN,
                          linestyle=PlotlyPlotting.Linestyle.DASHED))
        # yaxis.append(Axis(self.__energy_management_data.pv_power, label=EnergyManagementState.PV_POWER, color=Plotting.Color.BLUE,
        #                  linestyle=Plotting.Linestyle.DASH_DOT))
        # grid_power = [load + battery - pv for load, battery, pv in zip(data.power, self.__energy_management_data.load_power, self.__energy_management_data.pv_power)]
        grid_power = system_data.power + ems_data.load_power - ems_data.pv_power
        yaxis.append(Axis(grid_power, label='Total Site Power in W', color=PlotlyPlotting.Color.RED,
                          linestyle=PlotlyPlotting.Linestyle.DOTTED))
        yaxis.append(Axis(system_data.soc, label=SystemState.SOC, color=PlotlyPlotting.Color.GREEN,
                          linestyle=PlotlyPlotting.Linestyle.DOTTED))
        plot.lines(xaxis, yaxis, [3])
        self.extend_figures(plot.get_figures())

    @property
    def power_above_peak(self):
        data: EnergyManagementData = self.get_data()
        grid_power = self.__system_data.power + data.load_power - data.pv_power
        power_above_peak = grid_power - self.__max_power
        power_above_peak[power_above_peak < 0.0] = 0.0
        return power_above_peak

    @staticmethod
    def max_power_above_peak(power_above_peak) -> float:
        return max(0.0, get_max_for(power_above_peak))

    @staticmethod
    def get_average_power_above_peak_from(power_above_peak) -> float:
        power = power_above_peak[power_above_peak > 0.0]
        if len(power) == 0:
            return 0.0
        return sum(power) / len(power)

    def energy_events_above_peak(self, power_above_peak) -> [float]:
        energy_above_peak = power_above_peak * self.get_data().convert_watt_to_kWh
        energy_events: [float] = list()
        energy_event: float = 0.0
        for energy in energy_above_peak:
            if energy_event > 1e-5 and energy == 0.0:
                energy_events.append(energy_event)
                energy_event = 0.0
            else:
                energy_event += energy
        return energy_events

    @staticmethod
    def get_max_energy_event_above_peak_from(energy_events: [float]) -> float:
        if not energy_events:
            return 0.0
        return max(energy_events)

    @staticmethod
    def get_average_energy_event_above_peak_from(energy_events: [float]) -> float:
        if not energy_events:
            return 0.0
        return sum(energy_events) / len(energy_events)
