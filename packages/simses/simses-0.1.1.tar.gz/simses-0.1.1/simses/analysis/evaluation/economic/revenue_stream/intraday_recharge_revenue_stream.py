import numpy

from simses.analysis.data.energy_management_data import EnergyManagementData
from simses.analysis.data.system_data import SystemData
from simses.analysis.evaluation.economic.revenue_stream.revenue_stream import RevenueStream
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Unit, Description
from simses.commons.log import Logger
from simses.commons.profile.economic_profile.intraday_market import IntradayMarket
from simses.config.analysis.economic_analysis_config import EconomicAnalysisConfig


class IntradayRechargeRevenue(RevenueStream):
    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData,
                 economic_analysis_config: EconomicAnalysisConfig, market: IntradayMarket):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self.__time = energy_management_data.time
        self.__intraday_power = energy_management_data.idm_power
        self.__idm_price_profile: IntradayMarket = market
        if economic_analysis_config.idm_use_price_timeseries:
            self.__intraday_time, self.__intraday_price = self.__idm_price_profile.read_whole_file_adjusted(
                float(self._energy_management_data.time[0]), float(self._energy_management_data.time[-1]),
                float(self._energy_management_data.time[1]) - float(self._energy_management_data.time[0]))
        else:
            self.__intraday_price = [economic_analysis_config.idm_price for i in range(len(self.__time))]
        self.__system_data: SystemData = system_data
        self.__log: Logger = Logger(type(self).__name__)
        self.__intraday_power_avg = []
        self.__intraday_price_avg = []
        self.__intraday_revenue = []
        self.hour_to_sec = 60 * 60
        self.day_to_sec = self.hour_to_sec * 24
        self.year_to_sec = self.day_to_sec * 365

    def get_cashflow(self) -> numpy.ndarray:

        time = self.__time
        intraday_power = self.__intraday_power
        intraday_price = self.__intraday_price
        t = 0
        t_year_start = 0
        cashflow_fcr = 0
        intraday_power_avg = []
        intraday_price_avg = []
        cashflow_list_intraday = []
        intraday_price_scaling_factor = 1/1e3 * 1/self.hour_to_sec
        delta_ts = time[1] - time[0]

        while t < len(time):
            if time[t] - time[t_year_start] >= self.year_to_sec:
                intraday_power_avg.append(sum(intraday_power[t_year_start:t]) / (t - t_year_start + 1))
                intraday_price_avg.append(sum(intraday_price[t_year_start:t]) / (t - t_year_start + 1))
                cashflow_list_intraday.append(cashflow_fcr)
                t_year_start = t
                cashflow_fcr = 0
            cashflow_fcr += delta_ts * intraday_power[t] * intraday_price[t] * intraday_price_scaling_factor
            t += 1

        # Adding non-full year
        intraday_power_avg.append(sum(intraday_power[t_year_start:t]) / (t - t_year_start + 1))
        intraday_price_avg.append(sum(intraday_price[t_year_start:t]) / (t - t_year_start + 1))
        cashflow_list_intraday.append(cashflow_fcr)

        self.__intraday_power_avg = intraday_power_avg
        self.__intraday_price_avg = intraday_price_avg
        self.__intraday_revenue = cashflow_list_intraday

        return numpy.array(cashflow_list_intraday)

    def get_evaluation_results(self) -> [EvaluationResult]:
        key_results: [EvaluationResult] = list()
        key_results.append(EvaluationResult(Description.Economical.Intraday.REVENUE_YEARLY, Unit.EURO, self.__intraday_revenue))
        return key_results

    def get_assumptions(self) -> [EvaluationResult]:
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.Intraday.PRICE_AVERAGE, Unit.EURO, self.__intraday_price_avg))
        assumptions.append(EvaluationResult(Description.Economical.Intraday.POWER_AVERAGE, Unit.EURO, self.__intraday_power_avg))
        return assumptions

    def close(self):
        self.__log.close()
