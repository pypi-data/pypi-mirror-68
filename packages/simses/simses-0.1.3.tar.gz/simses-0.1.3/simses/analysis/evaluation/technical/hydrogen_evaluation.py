import numpy as np
import math as m

from simses.analysis.utils import get_positive_values_from, get_sum_for
from simses.analysis.data.hydrogen_data import HydrogenData
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.analysis.evaluation.technical.technical_evaluation import TechnicalEvaluation
from simses.commons.state.technology.hydrogen_state import HydrogenState
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig
from simses.simulation.storage_system.technology.hydrogen.constants.constants_hydrogen import ConstantsHydrogen


class HydrogenTechnicalEvaluation(TechnicalEvaluation):

    title = 'Hydrogen results'

    def __init__(self, data: HydrogenData, config: GeneralAnalysisConfig, path: str):
        super().__init__(data, config)
        title_extension: str = ' for system ' + self.get_data().id
        self.title += title_extension
        self.__result_path = path

    def evaluate(self):
        super().evaluate()
        self.append_result(EvaluationResult(Description.Technical.EQUIVALENT_FULL_CYCLES, Unit.NONE, self.equivalent_full_cycles))
        self.append_result(EvaluationResult(Description.Technical.DEPTH_OF_DISCHARGE, Unit.PERCENTAGE, self.depth_of_discharges))
        self.append_result(EvaluationResult(Description.Technical.ENERGY_THROUGHPUT, Unit.KWH, self.energy_throughput))
        self.append_result(EvaluationResult(Description.Technical.H2_PRODUCTION_EFFICIENCY_LHV, Unit.PERCENTAGE, self.h2_production_efficiency_lhv))
        self.print_results()

    @property
    def h2_production_efficiency_lhv(self) -> float:
        """
        Calculates the hydrogen production efficiency relative to its lower heating value

        Parameters
        -----------
            data: simulation results

        :return:
            float: h2 production efficiency
        """
        data: HydrogenData = self.get_data()
        timestep = data.time[1] - data.time[0]
        total_energy_pump_el = get_sum_for(data.power_pump_el) * timestep * 10 ** (-3) / 3600
        total_energy_compressor = get_sum_for(data.power_compressor) * timestep * 10 ** (-3) / 3600
        total_energy_gas_drying = get_sum_for(data.power_gas_drying) * timestep * 10 ** (-3) / 3600
        power_heating_1 = get_positive_values_from(data.power_water_heating_el)
        total_energy_heating = get_sum_for(power_heating_1) * timestep * 10 ** (-3) / 3600
        total_energy_reaction = get_sum_for(data.power) * timestep * 10 ** (-3) / 3600
        total_energy_h2_lhv = data.total_h2_production[-1] * ConstantsHydrogen.LHV_H2
        return total_energy_h2_lhv / (total_energy_pump_el + total_energy_compressor + total_energy_gas_drying + total_energy_heating
                + total_energy_reaction) * 100

    def plot(self) -> None:
        self.current_el_plotting()
        self.fulfillment_plotting()
        self.hydrogen_production_plotting()
        self.pressure_cathode_el_plotting()
        self.hydrogen_outflow_plotting()
        self.pressure_anode_el_plotting()
        self.temperature_el_plotting()
        self.power_water_heating_el_plotting()
        self.power_auxilliaries_el_plotting()
        # data: HydrogenData = self.get_data()
        # plot: Plotting = PlotlyPlotting(title=self.title, path=self.__result_path)
        # xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        # yaxis: [[Axis]] = list()
        # yaxis.append([Axis(data=data.soc, label=HydrogenState.SOC),
        #               Axis(data=data.power * 1000, label=HydrogenState.POWER)])
        # yaxis.append([Axis(data=data.temperature_el, label=HydrogenState.TEMPERATURE_EL),
        #               Axis(data=data.power_water_heating_el, label=HydrogenState.POWER_WATER_HEATING_EL)])
        #
        #
        # plot.subplots(xaxis=xaxis, yaxis=yaxis)
        # self.extend_figures(plot.get_figures())

    def current_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=HydrogenState.CURRENT_EL, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = [Axis(data=data.current_el, label=HydrogenState.CURRENT_EL)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def hydrogen_production_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=HydrogenState.HYDROGEN_PRODUCTION, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = [Axis(data=data.hydrogen_production, label=HydrogenState.HYDROGEN_PRODUCTION)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def pressure_cathode_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title='Pressures Cathode', path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.pressure_cathode_el, label=HydrogenState.PRESSURE_CATHODE_EL,
                          color=PlotlyPlotting.Color.RED, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.part_pressure_h2_el, label=HydrogenState.PART_PRESSURE_H2_EL,
                          color=PlotlyPlotting.Color.RED, linestyle=PlotlyPlotting.Linestyle.DOTTED))
        # yaxis.append(Axis(data=data.sat_pressure_h20_el, label=HydrogenState.SAT_PRESSURE_H2O_EL,
        #                   color=PlotlyPlotting.Color.BLUE, linestyle=PlotlyPlotting.Linestyle.DASHED))
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def pressure_anode_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title='Pressures Anode', path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.pressure_anode_el, label=HydrogenState.PRESSURE_ANODE_EL,
                          color=PlotlyPlotting.Color.GREEN, linestyle=PlotlyPlotting.Linestyle.SOLID))
        yaxis.append(Axis(data=data.part_pressure_o2_el, label=HydrogenState.PART_PRESSURE_O2_EL,
                          color=PlotlyPlotting.Color.GREEN, linestyle=PlotlyPlotting.Linestyle.DOTTED))
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def temperature_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=HydrogenState.TEMPERATURE_EL, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = [Axis(data=data.temperature_el, label=HydrogenState.TEMPERATURE_EL)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def power_water_heating_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title='Elektrolyzer Stack Heat', path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.power_water_heating_el, label=HydrogenState.POWER_WATER_HEATING_EL,
                          color=PlotlyPlotting.Color.BLUE))
        yaxis.append(Axis(data=data.convection_heat, label=HydrogenState.CONVECTION_HEAT,
                          color=PlotlyPlotting.Color.RED))
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())

    def power_auxilliaries_el_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title='Auxiliaries', path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data.power_water_heating_el, label=HydrogenState.POWER_WATER_HEATING_EL, color=PlotlyPlotting.Color.BLUE))
        yaxis.append(Axis(data.power_compressor, label=HydrogenState.POWER_COMPRESSOR, color=PlotlyPlotting.Color.BLACK))
        yaxis.append(Axis(data.power_gas_drying, label=HydrogenState.POWER_GAS_DRYING, color=PlotlyPlotting.Color.RED))
        yaxis.append(Axis(data.power_pump_el, label=HydrogenState.POWER_PUMP_EL, color=PlotlyPlotting.Color.MAGENTA))
        plot.lines(xaxis, yaxis, [2,3])
        self.extend_figures(plot.get_figures())

    def hydrogen_outflow_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title='Hydrogen outflow and total injection', path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = list()
        yaxis.append(Axis(data=data.hydrogen_outflow, label=HydrogenState.HYDROGEN_OUTFLOW))
        yaxis.append(Axis(data=data.total_h2_production, label=HydrogenState.TOTAL_HYDROGEN_PRODUCTION,
                          color=PlotlyPlotting.Color.GREEN))
        plot.lines(xaxis, yaxis, [1])
        self.extend_figures(plot.get_figures())

    def fulfillment_plotting(self):
        data: HydrogenData = self.get_data()
        plot: Plotting = PlotlyPlotting(title=HydrogenState.FULFILLMENT, path=self.__result_path)
        xaxis: Axis = Axis(data=Plotting.format_time(data.time), label=HydrogenState.TIME)
        yaxis: [Axis] = [Axis(data=data.fulfillment, label=HydrogenState.FULFILLMENT)]
        plot.lines(xaxis, yaxis)
        self.extend_figures(plot.get_figures())


