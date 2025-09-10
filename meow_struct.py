from typing import Generator, TypedDict

from .abstract_classes import MemoryReadAbs, ModuleAbs, ProcessAbs
from .pyMeow import r_bytes, open_process, get_process_path, get_module, enum_modules, process_exists


class MeowMemoryRead(MemoryReadAbs):
    def __init__(self, process: dict) -> None:
        self.process = process

    def read_memory(self, address: int, size: int) -> bytes:
        return r_bytes(self.process, address, size)


class MeowModule(ModuleAbs):
    def __init__(self, module: dict) -> None:
        self.module = module

    @property
    def name(self) -> str:
        return self.module.get("name", "")

    @property
    def base(self) -> int:
        return self.module.get("base", -1)

    @property
    def size(self) -> int:
        return self.module.get("size", -1)


class MeowProcess(ProcessAbs):
    def __init__(self, process_name: str):
        self.process = open_process(process_name)
        self.memory_read = MeowMemoryRead(self.process)

    @property
    def name(self) -> str:
        return self.process.get("name", "null")

    @property
    def pid(self) -> int:
        return self.process.get("pid", -1)

    @property
    def path(self) -> str:
        return get_process_path(self.process)

    def get_module(self, module_name: str) -> ModuleAbs:
        return MeowModule(get_module(self.process, module_name))

    def module_list(self) -> Generator[ModuleAbs, None, None]:
        return (MeowModule(module) for module in enum_modules(self.process))

    def alive_check(self) -> bool:
        return process_exists(self.process.get("name"))

