import math
from datetime import datetime

import numpy as np

from simses.analysis.data.data import Data
from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.evaluation_result import EvaluationResult, Description, Unit
from simses.commons.log import Logger
from simses.commons.utils.utils import format_float
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class TechnicalEvaluation(Evaluation):

    def __init__(self, data: Data, config: GeneralAnalysisConfig):
        super().__init__(data, config, config.technical_analysis)
        self.__log: Logger = Logger(type(self).__name__)

    def evaluate(self):
        self.append_result(EvaluationResult(Description.Technical.EFFICIENCY, Unit.PERCENTAGE, self.round_trip_efficiency))
        self.append_result(EvaluationResult(Description.Technical.MEAN_SOC, Unit.PERCENTAGE, self.mean_soc))
        self.append_result(EvaluationResult(Description.Technical.NUMBER_CHANGES_SIGNS, Unit.NONE, self.changes_of_sign))
        self.append_result(EvaluationResult(Description.Technical.RESTING_TIME_AVG, Unit.MINUTES, self.resting_times))
        self.append_result(EvaluationResult(Description.Technical.ENERGY_CHANGES_SIGN, Unit.PERCENTAGE, self.energy_swapsign))
        self.append_result(EvaluationResult(Description.Technical.FULFILLMENT_AVG, Unit.PERCENTAGE, self.average_fulfillment))
        self.append_result(EvaluationResult(Description.Technical.REMAINING_CAPACITY, Unit.PERCENTAGE, self.capacity_remaining))

    def plot(self) -> None:
        pass

    @property
    def round_trip_efficiency(self) -> float:

        """
        Calculates the round trip efficiency of the system/battery

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            round trip efficiency
        """
        data: Data = self.get_data()
        if data.charge_energy == 0.0:
            return 0.0
        a = data.discharge_energy
        b = data.energy_difference
        c = data.charge_energy

        # eta_ohne_anpassung = 100 * (data.discharge_energy + data.energy_difference) / data.charge_energy
        # eta_formel_genau = 100 * 0.5*((b*math.sqrt(4*a*c+b**2))/c**2 + 2*a/c + (b/c)**2)
        #
        # sum_pos_power = sum(data.power[data.power>0])/(60*60*1000)
        # sum_neg_power = sum(data.power[data.power<0])/(60*60*1000)

        # delta_soc = data.soc[-1] - data.soc[0]
        # e_nenn = data.initial_capacity
        # delta_energy = delta_soc * e_nenn
        #
        # test_power_pos = sum(data.power[data.power>0])
        # test_power_neg = sum(data.power[data.power<0])
        # test_sum_soc = sum(data.soc)

        # return 100 * (data.discharge_energy + data.energy_difference) / data.charge_energy
        efficiency = 100 * 0.5 * ((b * math.sqrt(4 * a * c + b ** 2)) / c ** 2 + 2 * a / c + (b / c) ** 2)
        if not 100 > efficiency > 0:
            self.__log.error(Description.Technical.EFFICIENCY + ' should be between 0 % and 100 %, but is ' +
                             str(format_float(efficiency)) + '%.'
                             + ' Perhaps is your simulation time too short for a accurate round trip efficiency')
        return efficiency

    @property
    def capacity_remaining(self) -> float:
        data: Data = self.get_data()
        return data.capacity[-1] / data.initial_capacity * 100.0

    @property
    def energy_throughput(self) -> float:
        data: Data = self.get_data()
        return data.charge_energy + data.discharge_energy

    @property
    def mean_soc(self) -> float:
        """
        Calculates the mean SOC of the system/battery

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average soc
        """
        data: Data = self.get_data()
        return 100 * data.average_soc

    @property
    def equivalent_full_cycles(self) -> float:
        """
        Calculates the number of full-equivalent cycles by dividing the amount of charged energy through the initial capacity

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            number of full-equivalent cycles
        """
        data: Data = self.get_data()
        return data.charge_energy / data.initial_capacity

    @property
    def depth_of_discharges(self) -> float:
        """
        Calculates the average depth of cycles in discharge direction

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average depth of cycles in discharge direction
        """
        data: Data = self.get_data()
        delta_soc = np.diff(data.soc)[abs(np.diff(data.soc)) > 1e-8]
        delta_soc_sign = np.sign(delta_soc)
        delta_soc_sign_diff = np.diff(delta_soc_sign)
        cycle_end = np.asarray(np.where(delta_soc_sign_diff != 0))
        cycle_start = cycle_end + 1
        cycle_start = np.insert(cycle_start, 0, 0)
        cycle_end = np.append(cycle_end, len(delta_soc) - 1)
        doc = np.asarray(
            [sum(delta_soc[cycle_start[counter]:cycle_end[counter] + 1]) for counter in range(0, len(cycle_start))])
        if len(doc) == 0:
            return 0
        if len(doc[doc < 0]) == 0:
            return 0
        doc_dis = abs(100 * doc[doc < 0].mean())
        return doc_dis

    @property
    def changes_of_sign(self) -> float:
        """
        Calculates the average number of changes of sign per day

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average number of changes of sign per day
        """
        data: Data = self.get_data()
        days_in_data = round(
            (datetime.fromtimestamp(data.time[-1]) - datetime.fromtimestamp(data.time[0])).total_seconds() / 86400)
        power_sign = np.sign(data.power)
        power_sign_nozero = power_sign[power_sign != 0]
        total_changes_of_sign = np.nansum(abs(np.diff(power_sign_nozero))) / 2
        if days_in_data > 0:
            daily_changes_of_sign = total_changes_of_sign / days_in_data
        else:
            daily_changes_of_sign = 'Less than one day simulated.'
        return daily_changes_of_sign

    @property
    def resting_times(self) -> float:
        """
        Calculates the average length of resting time of the system/battery

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average length of resting time in min
        """
        data: Data = self.get_data()
        resting_data = 1 * (abs(data.power) == 0)

        #data_power_temp = np.array([0, 0, 100, 100, 0, 0, -100, -100, 0, 0])
        #resting_data = 1 * (abs(data_power_temp) == 0)
        # resting_data = np.array([1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
        #test_begin = np.diff(resting_data) > 0

        #idx_begin_old = np.roll(np.diff(resting_data) > 0, 1)
        #idx_end_old = np.diff(resting_data) < 0

        #if resting_data[0] == 1:
        #    idx_begin_old[0] = 1
        #if resting_data[-1] == True:
        #    idx_end_old[-1] = True
        #times_length_old = np.where(idx_end_old)[0] +1 - np.where(idx_begin_old)[0]

        idx_begin = (np.diff(resting_data) > 0)
        idx_end = np.diff(resting_data) < 0
        if resting_data[0] == 1:
            idx_begin = np.insert(idx_begin, 0, True)
            idx_end = np.insert(idx_end, 0, False)
        if resting_data[-1] == True:
            idx_begin = np.append(idx_begin, False)
            idx_end = np.append(idx_end, True)
        times_length = np.where(idx_end)[0] - np.where(idx_begin)[0]
        timestep = data.time[1] - data.time[0]  # in seconds
        resting_times_length = times_length.mean() * timestep / 60
        return resting_times_length

    @property
    def energy_swapsign(self) -> float:
        """
        Calculates the average positive (charged) energy between changes of sign

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average charged energy between between changes of sign
        """
        data: Data = self.get_data()
        power_sign = np.sign(data.power)
        power = data.power

        index_of_end_before_change = np.asarray(np.where(np.diff(power_sign) != 0))
        if index_of_end_before_change.size == 0:
            return 0
        index_of_start_after_change = index_of_end_before_change + 1
        index_of_end_before_change = np.delete(index_of_end_before_change, 0)
        index_of_end_before_change = np.append(index_of_end_before_change, len(power_sign) - 1)

        timestep = data.time[1] - data.time[0]  # in seconds

        sums_list = []
        for i in range(len(index_of_end_before_change)):
            summed_energy = sum(power[index_of_start_after_change[0, i]:index_of_end_before_change[i] + 1]) * \
                            timestep / 3600 / 1000
            if summed_energy != 0:
                sums_list.append(summed_energy)

        nom_capacity = data.initial_capacity
        sums_list = np.asarray(sums_list)
        pos_energy_swapsign_norm = np.mean(sums_list[sums_list > 0]) / nom_capacity * 100  # in %

        return pos_energy_swapsign_norm

    @property
    def average_fulfillment(self) -> float:
        """
        Calculates the average fulfillment factor of the system/battery. How often can the battery/system charge/discharge the desired amount of power.

        Parameters
        ----------
            data : simulation results

        Returns
        -------
        float:
            average fulfillment factor
        """
        data: Data = self.get_data()
        return 100 * np.mean(data.storage_fulfillment)

    def close(self) -> None:
        self.__log.close()
