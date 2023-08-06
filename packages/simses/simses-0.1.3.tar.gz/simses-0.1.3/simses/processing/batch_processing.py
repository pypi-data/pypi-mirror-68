import multiprocessing
from abc import abstractmethod, ABC

from simses.constants_simses import ROOT_PATH, BATCH_DIR
from simses.commons.utils.utils import remove_all_files_from, create_directory_for
from simses.main import SimSES


class BatchProcessing(ABC, multiprocessing.Process):

    def __init__(self, path: str = ROOT_PATH + 'results/', batch_size: int = 1):
        super().__init__()
        create_directory_for(path)
        remove_all_files_from(path + BATCH_DIR)
        self._path: str = path
        self.__batch_size: int = batch_size

    @abstractmethod
    def _setup(self) -> [SimSES]:
        pass

    def run(self):
        started: [SimSES] = list()
        simulations: [SimSES] = self._setup()
        self.__check_simulation_names(simulations)
        for simulation in simulations:
            print('\rStarting ' + simulation.name)
            simulation.start()
            started.append(simulation)
            if len(started) >= self.__batch_size:
                self.__wait_for(started)
                started.clear()
        self.__wait_for(started)

    @staticmethod
    def __wait_for(simulations: [SimSES]):
        for simulation in simulations:
            simulation.join()

    @staticmethod
    def __check_simulation_names(simulations: [SimSES]) -> None:
        names: [str] = list()
        for simulation in simulations:
            name: str = simulation.name
            if name in names:
                raise Exception(name + ' is not unique. Please check your simulation setup!')
            names.append(name)
