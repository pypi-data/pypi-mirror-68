import numpy as np

from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.commons.state.system_state import SystemState
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class SystemTechnicalEvaluation(TechnicalEvaluation):

    power_title = 'System power'
    soc_title = 'System SOC'

    def __init__(self, data: SystemData, config: GeneralAnalysisConfig, path: str):
        super().__init__(data, config)
        title_extension: str = ' for system ' + self.get_data().id
        self.power_title += title_extension
        self.soc_title += title_extension
        self.__result_path = path

    def evaluate(self):
        super().evaluate()
        self.append_result(EvaluationResult(Description.Technical.PE_EFFICIENCY_DISCHARGE_MEAN, Unit.PERCENTAGE, self.mean_pe_efficiency_discharge()))
        self.append_result(EvaluationResult(Description.Technical.PE_EFFICIENCY_CHARGE_MEAN, Unit.PERCENTAGE, self.mean_pe_efficiency_charge()))
        self.print_results()

    def plot(self) -> None:
        self.power_plotting()
        self.soc_plotting()

    def soc_plotting(self):
        data: SystemData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.soc_title,  path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=SystemState.TIME)
        yaxis: [Axis] = [Axis(data.soc, label=SystemState.SOC)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def power_plotting(self):
        data: SystemData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=self.power_title, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=SystemState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data.dc_power * data.storage_fulfillment, label=SystemState.DC_POWER_DELIVERED,
                          color=PlotlyPlotting.Color.BLACK, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data.power, label=SystemState.AC_POWER_DELIVERED, color=PlotlyPlotting.Color.GREEN,
                          linestyle=PlotlyPlotting.Linestyle.DASHED))
        yaxis.append(Axis(data.dc_power, label=SystemState.DC_POWER, color=PlotlyPlotting.Color.RED,
                          linestyle=PlotlyPlotting.Linestyle.DASHED))
        yaxis.append(Axis(data.ac_power_target, label=SystemState.AC_POWER, color=PlotlyPlotting.Color.BLUE,
                          linestyle=PlotlyPlotting.Linestyle.DASH_DOT))
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def mean_pe_efficiency_discharge(self) -> float:
        """
        Calculates the average power electronics efficiency when discharging.
        For every discharging step the efficiency is calculated and in the end the mean value of all efficiencies.

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average power electronics efficiency (discharge)
        """
        data: SystemData = self.get_data()
        dc_pe_power = data.dc_power[:] * data.storage_fulfillment
        ac_pe_power = data.ac_pe_power[:]
        ac_pe_power[ac_pe_power >= 0] = np.nan
        dc_pe_power[dc_pe_power >= 0] = np.nan
        if len(ac_pe_power) == 0 or len(dc_pe_power) == 0:
            return np.nan
        if np.isnan(ac_pe_power).all() or np.isnan(dc_pe_power).all():
            return np.nan
        mean_pe_eta_discharge = np.nanmean(ac_pe_power / dc_pe_power)
        return 100 * mean_pe_eta_discharge

    def mean_pe_efficiency_charge(self) -> float:
        """
        Calculates the average power electronics efficiency when charging.
        For every charging step the efficiency is calculated and in the end the mean value of all efficiencies.

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average power electronics efficiency (charge)
        """
        data: SystemData = self.get_data()
        dc_pe_power = data.dc_power[:] * data.storage_fulfillment
        ac_pe_power = data.ac_pe_power[:]
        ac_pe_power[ac_pe_power <= 0] = np.nan
        dc_pe_power[dc_pe_power <= 0] = np.nan
        if len(ac_pe_power) == 0 or len(dc_pe_power) == 0:
            return np.nan
        if np.isnan(ac_pe_power).all() or np.isnan(dc_pe_power).all():
            return np.nan
        mean_pe_eta_charge = np.nanmean(dc_pe_power / ac_pe_power)
        return 100 * mean_pe_eta_charge
