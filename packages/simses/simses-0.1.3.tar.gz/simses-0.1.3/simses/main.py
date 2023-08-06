import threading
from configparser import ConfigParser
from multiprocessing import Queue

from simses.constants_simses import ROOT_PATH
from simses.analysis.analysis import StorageAnalysis
from simses.commons.state.system_state import SystemState
from simses.commons.utils.utils import create_directory_for
from simses.config.log_config import LogConfig
from simses.simulation.simulation import StorageSimulation


class SimSES(threading.Thread):

    def __init__(self, path: str, name: str, do_simulation: bool = True, do_analysis: bool = True,
                 simulation_config: ConfigParser = None, analysis_config: ConfigParser = None, queue: Queue = None):
        super().__init__()
        self.__do_simulation = do_simulation
        self.__do_analysis = do_analysis
        self.__name: str = name
        path = path + name + '/'
        if self.__do_simulation:
            create_directory_for(path)
            self.__storage_simulation: StorageSimulation = StorageSimulation(path, simulation_config, queue)
        if self.__do_analysis:
            self.__storage_analysis: StorageAnalysis = StorageAnalysis(path, analysis_config)

    @property
    def name(self) -> str:
        return self.__name

    def run(self) -> None:
        self.run_simulation()
        self.run_analysis()
        self.close()

    def run_one_simulation_step(self, time: float, power: float = None) -> None:
        self.__storage_simulation.run_one_step(ts=time, power=power)

    def evaluate_multiple_simulation_steps(self, start: float, timestep: float, power: list) -> [SystemState]:
        return self.__storage_simulation.evaluate_multiple_steps(start, timestep, power)

    def run_simulation(self) -> None:
        if self.__do_simulation:
            self.__storage_simulation.run()

    def run_analysis(self) -> None:
        if self.__do_analysis:
            self.__storage_analysis.run()

    @property
    def state(self) -> SystemState:
        return self.__storage_simulation.state

    def close(self) -> None:
        self.close_simulation()
        self.close_analysis()

    def close_simulation(self) -> None:
        if self.__do_simulation:
            self.__storage_simulation.close()

    def close_analysis(self) -> None:
        if self.__do_analysis:
            self.__storage_analysis.close()

    @classmethod
    def set_log_config(cls, configuration: ConfigParser):
        LogConfig.set_config(configuration)

    def get_storage_simulation(self) -> StorageSimulation:
        return self.__storage_simulation


if __name__ == "__main__":
    # minimum working example
    # config: ConfigParser = ConfigParser()
    # config.add_section('GENERAL')
    # config.set('GENERAL', 'TIME_STEP', '60')
    result_path: str = ROOT_PATH + 'results/'
    simulation_name: str = 'simses_1'
    simses: SimSES = SimSES(result_path, simulation_name, do_simulation=True, do_analysis=True)
    # simses: SimSES = SimSES(result_path, simulation_name, do_simulation=True, do_analysis=True, simulation_config=config)
    simses.start()
    simses.join()
