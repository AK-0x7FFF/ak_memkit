from ctypes.wintypes import HANDLE
from typing import Generator

from winappdbg.module import Module
from winappdbg.process import Process
from winappdbg.system import System

from neac_controller import NeacDriverManager
from .abstract_classes import MemoryReadAbs, ModuleAbs, ProcessAbs


class NeacMemoryRead(MemoryReadAbs):
    def __init__(self, driver: NeacDriverManager, pid: int) -> None:
        self.driver = driver
        self.pid = pid

    def read_memory(self, address: int, size: int) -> bytes | None:
        return self.driver.read_process_memory(self.pid, address, size)


class NeacModule(ModuleAbs):
    def __init__(self, module: Module):
        self.module: Module = module

    @property
    def name(self) -> str:

        return self.module.get_filename().split("\\")[-1]

    @property
    def base(self) -> int:
        return self.module.get_base()

    @property
    def size(self) -> int:
        return self.module.get_size()


class NeacProcess(ProcessAbs):
    def __init__(self, process_name: str) -> None:
        self.driver = NeacDriverManager()
        if not (self.driver.start_driver() and self.driver.connect()):
            raise
        self.process = self.__get_process(process_name)
        self.__pid = self.process.get_pid()
        self.__memory_read = NeacMemoryRead(self.driver, self.__pid)

    def __del__(self) -> None:
        self.driver.disconnect()

    @staticmethod
    def __get_process(process_name: str) -> Process | None:
        system = System()
        system.scan_processes_fast()
        for process in system:
            name = process.get_filename()
            if name is None:
                continue
            if name.split("\\")[-1].lower() == process_name.lower():
                return process
        return None


    @property
    def name(self) -> str:
        return self.process.get_filename().split("\\")[-1].lower()

    @property
    def pid(self) -> int:
        return self.__pid

    @property
    def path(self) -> str:
        return self.process.get_filename()

    def get_module(self, module_name: str) -> ModuleAbs:
        return NeacModule(self.process.get_module_by_name(module_name))

    def module_list(self) -> Generator[ModuleAbs, None, None]:
        return (NeacModule(module) for module in self.process.iter_modules())

    @property
    def memory_read(self) -> MemoryReadAbs:
        return self.__memory_read

    def alive_check(self) -> bool:
        ...