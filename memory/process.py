from typing import Optional, Literal

from .abstract_classes import ProcessAbs


class Process:
    _global_instance: Optional[ProcessAbs] = None

    @staticmethod
    def _create_instance(process_name: str, mode: Literal["meow", "fpga"]) -> ProcessAbs | None:
        match mode:
            case "meow":
                from .meow import MeowProcess
                return MeowProcess(process_name)
            case "neac":
                from .neac import NeacProcess
                return NeacProcess(process_name)
            case "fpga":
                from .fpga import FpgaProcess
                return FpgaProcess(process_name)

    @classmethod
    def create_global_instance(cls, process_name: str, mode: Literal["meow", "fpga"]) -> ProcessAbs | None:
        if cls._global_instance is not None: return None

        cls._global_instance = cls._create_instance(process_name, mode)
        return cls._global_instance

    @classmethod
    def get_global_instance(cls) -> ProcessAbs | None:
        if cls._global_instance is None: return None
        return cls._global_instance

    def __new__(cls, process_name: str, mode: Literal["meow", "fpga"]) -> ProcessAbs | None:
        return cls._create_instance(process_name, mode)



