import multiprocessing
import sys
import time
from configparser import ConfigParser
from multiprocessing import Queue

from simses.commons.console_printer import ConsolePrinter
from simses.commons.utils.utils import format_float
from simses.main import SimSES
from simses.processing.batch_processing import BatchProcessing


class ExampleBatchProcessing(BatchProcessing):

    # number of simulations running on the same core
    BATCH_SIZE: int = 2

    # number of simulations running simultaneously on the same core
    SIM_SIZE: int = 1

    # total number of simulations
    NUMBER_OF_SIMULATIONS: int = 0

    # Example for config setup
    storage_1: str = 'system_1,NoLossDcDcConverter,storage_1\n'
    storage_2: str = 'system_1,NoLossDcDcConverter,storage_2\n'
    storage_3: str = 'system_1,NoLossDcDcConverter,storage_3\n'
    storage_4: str = 'system_1,NoLossDcDcConverter,storage_4\n'

    config_set: dict = dict()
    config_set['storage_1'] = storage_1
    config_set['storage_2'] = storage_2
    config_set['storage_3'] = storage_3
    config_set['storage_4'] = storage_4
    config_set['hybrid_1'] = storage_1 + storage_2
    config_set['hybrid_2'] = storage_3 + storage_4

    def __init__(self, queue: Queue):
        super().__init__(batch_size=self.SIM_SIZE)
        self.__queue: Queue = queue
        self.__config_set: dict = self.__generate_local_config_set()

    def __generate_local_config_set(self) -> dict:
        config_set: dict = dict()
        while len(config_set) < self.BATCH_SIZE:
            try:
                key, value = self.config_set.popitem()
                config_set[key] = value
            except KeyError:
                break
        return config_set

    def _setup(self) -> [SimSES]:

        # Example for varying input profiles
        # file_names: [str] = list()
        # file_name_pattern: str = 'SBAP_Industry_Input_Profiles_median_ip_'
        # file_name_extension: str = '.csv'
        # config: ProfileConfig = ProfileConfig(None)
        # load_profile_path: str = config.power_profile_dir
        # for file in os.listdir(load_profile_path):
        #     if file.endswith(file_name_extension) and file.startswith(file_name_pattern):
        #         file_names.append(file)

        # Optional: print configs
        print(self.__config_set)
        # print(file_names)

        # Example for setting up simulation threads with config variation
        simulations: [SimSES] = list()
        for name, value in self.__config_set.items():
            config: ConfigParser = ConfigParser()
            config.add_section('STORAGE_SYSTEM')
            config.set('STORAGE_SYSTEM', 'STORAGE_SYSTEM_DC', value)
            simulations.append(SimSES(self._path, name, do_simulation=True, do_analysis=True,
                                      simulation_config=config, queue=self.__queue))
        ExampleBatchProcessing.NUMBER_OF_SIMULATIONS += len(simulations)
        return simulations

if __name__ == "__main__":
    jobs: [BatchProcessing] = list()
    queue: Queue = Queue(maxsize=10)
    printer: ConsolePrinter = ConsolePrinter(queue)
    while ExampleBatchProcessing.config_set:
        jobs.append(ExampleBatchProcessing(queue))
    cpu_count: int = multiprocessing.cpu_count()
    job_count: int = len(jobs)
    print('CPU cores: ' + str(cpu_count) + ', parallel simulations: ' + str(job_count))
    if job_count > cpu_count:
        sys.stderr.write('WARNING: Number of jobs exceed number of cpu cores! Performance decrease possible!')
        sys.stderr.flush()
    printer.start()
    start = time.time()
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    duration: float = (time.time() - start) / 60.0
    print('\nMultiprocessing finished in ' + format_float(duration))# + ' min (' +
    #       format_float(duration / ExampleBatchProcessing.NUMBER_OF_SIMULATIONS) + ' min per simulation)')
