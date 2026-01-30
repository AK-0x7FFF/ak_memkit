from typing import Generator

from memprocfs import FLAG_NOCACHE, FLAG_NOPAGING
from memprocfs.vmmpyc import VmmVirtualMemory, VmmModule, Vmm, VmmProcess

from .abstract_classes import MemoryReadAbs, ModuleAbs, ProcessAbs


class FpgaMemoryRead(MemoryReadAbs):
    def __init__(self, memory: VmmVirtualMemory) -> None:
        self.memory = memory

    def read_memory(self, address: int, size: int) -> bytes | None:
        return self.memory.read(address, size, FLAG_NOCACHE | FLAG_NOPAGING)


class FpgaModule(ModuleAbs):
    def __init__(self, module: VmmModule):
        self.module = module

    @property
    def name(self) -> str:
        return self.module.name

    @property
    def base(self) -> int:
        return self.module.base

    @property
    def size(self) -> int:
        return self.module.image_size


class FpgaProcess(ProcessAbs):
    def __init__(self, process_name: str) -> None:
        self.device: Vmm = Vmm([
            '-device', 'fpga',
            '-disable-python', '-disable-symbols', '-disable-symbolserver', '-disable-yara',
            '-disable-yara-builtin',
            '-debug-pte-quality-threshold', '64'
        ])
        self.process: VmmProcess = self.device.process(process_name)
        self.__memory_read = FpgaMemoryRead(self.process.memory)

    @property
    def name(self) -> str:
        return self.process.name

    @property
    def pid(self) -> int:
        return self.process.pid

    @property
    def path(self) -> str:
        return self.process.pathuser

    def get_module(self, module_name: str) -> ModuleAbs:
        return FpgaModule(self.process.module(module_name))

    def module_list(self) -> Generator[ModuleAbs, None, None]:
        return (FpgaModule(module) for module in self.process.module_list())

    @property
    def memory_read(self) -> MemoryReadAbs:
        return self.__memory_read

    def alive_check(self) -> bool:
        ...