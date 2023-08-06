import webbrowser

from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.plotting.plotting import Plotting
from simses.config.analysis.general_analysis_config import GeneralAnalysisConfig


class EvaluationMerger:

    OUTPUT_NAME: str = 'merged.html'

    def __init__(self, result_path: str, config: GeneralAnalysisConfig):
        self.__file_name = result_path + '/' + self.OUTPUT_NAME
        self.__merge_results: bool = config.merge_analysis

    def merge(self, evaluations: [Evaluation]) -> None:
        """
        Writes html file from evaluation results and figures.

        Parameters:
            evaluations:   List of evaluations.
        """

        if not self.__merge_results:
            return
        with open(self.__file_name, 'w') as outfile:
            outfile.write("<!DOCTYPE html><html><head></head><body>")
            for evaluation in evaluations:
                if evaluation.should_be_considered:
                    outfile.write("<section><b>"+evaluation.get_file_name()+"</b></section>")
                    for result in evaluation.evaluation_results:
                        outfile.write(result.to_console() + "<br>")
                    for figure in evaluation.get_figures():
                        outfile.write(Plotting.convert_to_html(figure))
                    outfile.write("<br><br>")
            outfile.write("</body></html>")
        webbrowser.open(self.__file_name, new=2)  # open in new tab
