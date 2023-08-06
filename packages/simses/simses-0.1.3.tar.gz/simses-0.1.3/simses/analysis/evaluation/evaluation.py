import csv
from abc import ABC, abstractmethod

from simses.analysis.data.data import Data
from simses.analysis.evaluation.evaluation_result import EvaluationResult
from simses.commons.utils.utils import create_directory_for
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class Evaluation(ABC):

    EXT: str = '.csv'

    def __init__(self, data: Data, config: GeneralAnalysisConfig, do_evaluation: bool):
        self.__data: Data = data
        self.__do_evaluation: bool = do_evaluation
        self.__do_plotting: bool = config.plotting and do_evaluation
        self._print_to_console: bool = config.print_result_to_console and do_evaluation
        self.__export_analysis_to_csv: bool = config.export_analysis_to_csv and do_evaluation
        self.__export_analysis_to_batch: bool = config.export_analysis_to_batch and do_evaluation
        self.__file_name: str = type(self).__name__ + self.__data.id + self.EXT
        self.__evaluation_results: [EvaluationResult] = list()
        self.__figures: list = list()

    @property
    def evaluation_results(self) -> [EvaluationResult]:
        return self.__evaluation_results

    def append_result(self, evaluation_result: EvaluationResult) -> None:
        self.__evaluation_results.append(evaluation_result)

    def extend_results(self, evaluation_results: [EvaluationResult]) -> None:
        self.__evaluation_results.extend(evaluation_results)

    def append_figure(self, figure) -> None:
        self.__figures.append(figure)

    def extend_figures(self, figures: list) -> None:
        self.__figures.extend(figures)

    def get_data(self):
        return self.__data

    def get_figures(self) -> list:
        return self.__figures

    def get_file_name(self) -> str:
        return self.__file_name

    @property
    def get_name(self) -> str:
        return type(self.__data).__name__

    @property
    def should_be_considered(self) -> bool:
        return self.__do_evaluation

    def run(self) -> None:
        if self.__do_evaluation:
            self.evaluate()
            if self.__do_plotting:
                self.plot()

    @abstractmethod
    def evaluate(self) -> None:
        pass

    @abstractmethod
    def plot(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def print_results(self):
        if not self._print_to_console:
            return
        print('\n[' + str(self.get_name).upper() + ' ANALYSIS]' + ' (System ' + self.__data.id + ')')
        for evaluation_result in self.evaluation_results:
            print(evaluation_result.to_console())

    def write_to_csv(self, path: str) -> None:
        if not self.__export_analysis_to_csv:
            return
        file = path + self.__file_name
        with open(file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for evaluation_result in self.evaluation_results:
                writer.writerow(evaluation_result.to_csv())

    def write_to_batch(self, path: str, name: str, run: str):
        if not self.__export_analysis_to_batch:
            return
        create_directory_for(path)
        for evaluation_result in self.evaluation_results:
            file_name = path + evaluation_result.description + self.EXT
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow([name, run, type(self).__name__, self.__data.id, evaluation_result.value,
                                 evaluation_result.unit])
