from __future__ import annotations

from functools import wraps
from typing import Literal, Callable, TypeVar

from deprecated import deprecated

from .abstract_classes import ProcessAbs


class Process:
    _instance: ProcessAbs | None = None
    _mode: Literal["meow", "neac", "fpga"] = None
    _T = TypeVar("_T")

    @staticmethod
    def mode_initialized_check(func: _T | None = None) -> _T | bool:
        if func is None:
            return Process._mode is not None

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not Process._mode:
                raise RuntimeError("Read mode not initialized, use Process.set_mode() instead.")

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def process_initialize_check(func: _T | None = None) -> _T | bool:
        if func is None:
            return Process._instance is not None

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not Process._instance:
                raise RuntimeError("Process not initialized, use create_instance() instead.")

            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def get_mode(cls) -> Literal["meow", "neac", "fpga"]:
        return cls._mode

    @classmethod
    def set_mode(cls, mode: Literal["meow", "neac", "fpga"]) -> type[Process]:
        cls._mode = mode
        return cls

    @classmethod
    def _create_instance(cls, process_name: str) -> ProcessAbs | None:
        match cls._mode:
            case "meow":
                from .meow import MeowProcess
                return MeowProcess(process_name)
            case "neac":
                from .neac import NeacProcess
                return NeacProcess(process_name)
            case "fpga":
                from .fpga import FpgaProcess
                return FpgaProcess(process_name)
            case _:
                raise ValueError()

    @classmethod
    def create(cls, process_name: str, mode: Literal["meow", "neac", "fpga"] | None = None) -> ProcessAbs | None:
        if mode is not None:
            cls.set_mode(mode)

        cls.mode_initialized_check(lambda: ...)

        cls._instance = cls._create_instance(process_name)
        return cls._instance

    @classmethod
    def get(cls) -> ProcessAbs | None:
        return cls._instance


    @classmethod
    @deprecated(reason="嘛。。結構關係沒法實現多進程讀取力，用 create_instance() 嘛")
    def create_global_instance(cls, process_name: str, mode: Literal["meow", "neac", "fpga"]) -> ProcessAbs | None:
        return cls.create(process_name, mode)

    @classmethod
    @deprecated(reason="嘛。。結構關係沒法實現多進程讀取力，用 get_instance() 嘛")
    def get_global_instance(cls) -> ProcessAbs | None:
        return cls.get()





