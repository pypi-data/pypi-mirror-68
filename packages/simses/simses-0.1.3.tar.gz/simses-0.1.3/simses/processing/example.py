import multiprocessing
import time
from configparser import ConfigParser
from multiprocessing import Queue

from simses.commons.console_printer import ConsolePrinter
from simses.commons.utils.utils import format_float
from simses.main import SimSES
from simses.processing.batch_processing import BatchProcessing


class ExampleBatchProcessing(BatchProcessing):

    # number of simulations running simultaneously on the same core
    SIM_SIZE: int = 1

    def __init__(self, config_set: dict, printer_queue: Queue):
        super().__init__(batch_size=self.SIM_SIZE)
        self.__printer_queue: Queue = printer_queue
        self.__config_set: dict = config_set

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
                                      simulation_config=config, queue=self.__printer_queue))
        return simulations


def check_running_process(processes: [multiprocessing.Process], max_parallel_processes: int) -> None:
    while True:
        running_jobs: int = 0
        for process in processes:
            if process.is_alive():
                running_jobs += 1
        if running_jobs < max_parallel_processes:
            break
        time.sleep(1)


def generate_config_set() -> dict:
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
    return config_set


if __name__ == "__main__":
    config_set: dict = generate_config_set()
    printer_queue: Queue = Queue(maxsize=len(config_set) * 2)
    printer: ConsolePrinter = ConsolePrinter(printer_queue)
    jobs: [BatchProcessing] = list()
    for key, value in config_set.items():
        jobs.append(ExampleBatchProcessing({key: value}, printer_queue))
    printer.start()
    started: [BatchProcessing] = list()
    max_parallel_processes: int = multiprocessing.cpu_count()
    start = time.time()
    for job in jobs:
        job.start()
        started.append(job)
        check_running_process(started, max_parallel_processes)
    for job in jobs:
        job.join()
    duration: float = (time.time() - start) / 60.0
    job_count: int = len(jobs)
    print('\nMultiprocessing finished ' + str(job_count) + ' simulations in ' + format_float(duration) + ' min '
          '(' + format_float(duration / job_count) + ' min per simulation)')
