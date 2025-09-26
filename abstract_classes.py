from abc import ABC, abstractmethod
from struct import unpack
from typing import Generator


class MemoryReadAbs(ABC):
    @staticmethod
    def unpack_byte(byte: bytes, format_str: str) -> bool | int | float | bytes | str | None:
        if byte is None or not len(byte): return None

        try: return unpack("<" + format_str, byte)[0]
        except Exception as err: return None

    @abstractmethod
    def read_memory(self, address: int, size: int) -> bytes | None: ...

    def read_bool(self, address: int) -> bool | None:
        return self.unpack_byte(self.read_memory(address, 1), "?")

    def read_i8(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 1), "b")

    def read_u8(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 1), "B")

    def read_i16(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 2), "h")

    def read_u16(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 2), "H")

    def read_i32(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 4), "i")

    def read_u32(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 4), "I")

    def read_i64(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 8), "q")

    def read_u64(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 8), "Q")

    def read_f32(self, address: int) -> float | None:
        return self.unpack_byte(self.read_memory(address, 4), "f")

    def read_vec(self, address: int, size: int) -> list[float] | None:
        byte = self.read_memory(address, 4 * size)
        if byte is None or not len(byte): return None

        try: return list(unpack("<%if" % size, byte))
        except Exception: return None

    def read_str(self, address: int, byte_size: int = 50) -> str | None:
        byte = self.read_memory(address, byte_size)
        if byte is None or not len(byte): return None

        try: return byte.split(b"\x00")[0].decode("utf-8")
        except Exception: return None


class ModuleAbs(ABC):
    def __repr__(self) -> str:
        return "%s<name=%s base=%s size=%s>" % (self.__class__.__name__, self.name, self.base, self.size)

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def base(self) -> int: ...

    @property
    @abstractmethod
    def size(self) -> int: ...


class ProcessAbs(ABC):
    @abstractmethod
    def __init__(self, process_name: str) -> None: ...

    def __repr__(self) -> str:
        return "%s<name=%s pid=%s>" % (self.__class__.__name__, self.name, self.pid)

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def pid(self) -> int: ...

    @property
    @abstractmethod
    def path(self) -> str: ...

    @abstractmethod
    def get_module(self, module_name: str) -> ModuleAbs: ...

    @abstractmethod
    def module_list(self) -> Generator[ModuleAbs, None, None]: ...

    memory_read: MemoryReadAbs