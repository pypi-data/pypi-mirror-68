from simses.analysis.evaluation.evaluation import Evaluation
from simses.analysis.evaluation.plotting.axis import Axis
from simses.analysis.evaluation.plotting.plotly_plotting import PlotlyPlotting
from simses.analysis.evaluation.plotting.plotting import Plotting


class BatchComparisonPlotting(Evaluation):

    title = 'Comparison Results'
    plot_param = list()
    data = list()
    path ='C:/PythonPlots/'

    def __init__(self, bc_data: list, param):
        # super().__init__(data, self.EXPORT_TO_CSV)
        self.data = bc_data
        self.plot_param = param
        #  title_extension: str = ' for system ' + self.get_data().id
        self.title = 'Comparison'
        # self.__result_path = path

    def evaluate(self):
        pass

    def plot(self):
        data = self.data
        # df = pd.DataFrame(data)
        df = data
        plot_param = self.plot_param
        plot: Plotting = PlotlyPlotting(title=self.title, path=self.path)
        xaxis: Axis = Axis(data=list(range(0, len(df[0]))), label='Plot no.')
        yaxis: [Axis] = list()
        print(plot_param)

        for i in range(0,len(plot_param)):
            print(df)
            label_now = plot_param[i]
            yaxis.append(Axis(data=df[i], label=label_now, color=PlotlyPlotting.Color.BLACK, linestyle=PlotlyPlotting.Linestyle.SOLID))

#           yaxis.append([Axis(data=df, label=plot_param(i))])
        # plot.subplots(xaxis=xaxis, yaxis=yaxis)
        plot.lines(xaxis, yaxis)

    def close(self) -> None:
        pass
