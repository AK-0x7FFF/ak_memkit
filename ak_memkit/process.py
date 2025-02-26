from abc import ABC, abstractmethod
from typing import Generator, Type, Self, Union

from .abstract_classes import ModuleAbs, ProcessAbs


@lambda cls: cls()
class Process:
    def __init__(self):
        self._process_class: Type[ProcessAbs] | None = None
        self._process: ProcessAbs | None = None

    def meow_mode(self) -> Self:
        from .meow_struct import MeowProcess

        self._process_class = MeowProcess
        return self

    def fpga_mode(self) -> Self:
        from .fpga_struct import FpgaProcess

        self._process_class = FpgaProcess
        return self

    def __call__(self, process_name: str) -> Self:
        if self._process_class is None: raise RuntimeError()

        self._process = self._process_class(process_name)
        global Process
        Process = None

        return self

    def __getattr__(self, item):
        if self._process_class is None or self._process is None: raise RuntimeError("Process is not setup.")
        return getattr(self._process, item)


Process: Union["Process", ProcessAbs]



