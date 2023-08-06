import os
import sys
import time
from configparser import ConfigParser
from multiprocessing import Queue
from queue import Full

from simses.commons.console_printer import ConsolePrinter
from simses.commons.data.data_handler import DataHandler
from simses.commons.log import Logger
from simses.commons.state.system_state import SystemState
from simses.commons.utils.utils import format_float
from simses.config.simulation.general_config import GeneralSimulationConfig
from simses.simulation.energy_management.energy_management import EnergyManagement
from simses.simulation.storage_system.storage_circuit import StorageCircuit


class StorageSimulation:

    def __init__(self, path: str, config: ConfigParser, queue: Queue):
        self.__path = path
        self.__log = Logger(__name__)
        self.__config = GeneralSimulationConfig(config)
        self.__data_export = DataHandler(path, self.__config)
        self.__energy_management: EnergyManagement = EnergyManagement(self.__data_export, config)
        self.__storage_system = StorageCircuit(self.__data_export, config)
        self.__name: str = os.path.basename(os.path.dirname(self.__path))
        self.__queue: Queue = queue
        self.__send_register_signal()
        self.__max_loop = self.__config.loop
        self.__start = self.__config.start
        self.__end = self.__config.end
        self.__duration = self.__end - self.__start
        self.__timestep = self.__config.timestep  # sec
        self.__timesteps_per_hour = 3600 / self.__timestep

    def run(self):
        self.__log.info('start')
        sim_start = time.time()
        ts_performance = []
        try:
            loop = 0
            ts = self.__start
            while loop < self.__max_loop:
                self.__log.info('Loop: ' + str(loop))
                ts_adapted = loop * self.__duration
                while ts <= (ts_adapted + self.__end) - self.__timestep:
                    ts_before = time.time()
                    ts += self.__timestep
                    self.run_one_step(ts, ts_adapted)
                    ts_performance.append(time.time() - ts_before)
                    self.__print_progress(ts)
                loop += 1
                if loop < self.__max_loop:
                    self.__energy_management: EnergyManagement = self.__energy_management.create_instance()
        except TypeError as err:
            raise err
        finally:
            self.close()
            self.__print_end(ts_performance, sim_start)

    def __print_progress(self, tstmp: float) -> None:
        progress = (tstmp - self.__start) / (self.__duration * self.__max_loop) * 100
        line: str = '|%-20s| ' % ('#' * round(progress / 5)) + format_float(progress, 1) + '%'
        output: dict = {self.__name: line}
        if self.__queue is None:
            sys.stdout.write('\r' + str(output))
            sys.stdout.flush()
        self.__put_to_queue(output)

    def __put_to_queue(self, output: dict, blocking: bool = False) -> None:
        if self.__queue is not None:
            try:
                if blocking:
                    self.__queue.put(output)
                else:
                    self.__queue.put_nowait(output)
            except Full:
                return

    def __send_stop_signal(self) -> None:
        self.__put_to_queue({self.__name: ConsolePrinter.STOP_SIGNAL}, blocking=True)

    def __send_register_signal(self) -> None:
        self.__put_to_queue({self.__name: ConsolePrinter.REGISTER_SIGNAL}, blocking=True)

    def __print_end(self, ts_performance: list, sim_start: float) -> None:
        sim_end = time.time()
        duration: str = format_float(sim_end - sim_start)
        duration_per_step: str = format_float(sum(ts_performance) * 1000 / len(ts_performance))
        self.__log.info('100.0% done. Duration in sec: ' + duration)
        self.__log.info('Duration per step in ms:      ' + duration_per_step)
        print('\r[' + self.__name + ': |%-20s| ' % ('#' * 20) + '100.0%]')
        print('          Duration in s: ' + duration)
        print('Duration per step in ms: ' + duration_per_step)

    def run_one_step(self, ts: float, ts_adapted: float = 0, power: float = None) -> None:
        state = self.__storage_system.state
        if not self.__data_export.is_alive():
            self.__data_export.start()
        self.__data_export.transfer_data(state.to_export())
        if power is None:
            power = self.__energy_management.next(ts - ts_adapted, state)
            self.__energy_management.export(ts)
        self.__storage_system.update(ts, power)

    def evaluate_multiple_steps(self, start: float, timestep: float, power: list) -> [SystemState]:
        res: [SystemState] = list()
        ts = start
        for pow in power:
            self.run_one_step(ts=ts, power=pow)
            res.append(self.state)
            ts += timestep
        return res

    @property
    def state(self) -> SystemState:
        return self.__storage_system.state

    def get_storage_system(self) -> StorageCircuit:
        return self.__storage_system

    def close(self) -> None:
        self.__log.info('closing')
        self.__data_export.transfer_data(self.__storage_system.state.to_export())
        self.__send_stop_signal()
        self.__config.write_config_to(self.__path)
        self.__log.close()
        self.__data_export.close()
        self.__energy_management.close()
        self.__storage_system.close()
