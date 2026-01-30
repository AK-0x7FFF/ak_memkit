from __future__ import annotations

from functools import wraps
from logging import warning
from typing import Self, Any, Callable, Sequence


from .memory.abstract_classes import ProcessAbs
from .memory.process import Process
from .vec import Vec2, Vec3



class AddressCacheSystem:
    cache_enable: bool = True
    _cache: dict[int, dict[int, Any]] = dict()

    @staticmethod
    def caching_decorator(func: Callable) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(address_object: "AddressMemoryRead", *args, **kwargs) -> Any:
            if not AddressCacheSystem.cache_enable:
                return func(address_object, *args, **kwargs)

            try:
                data_type = hash(func.__name__)
                value = AddressCacheSystem._cache.get(address_object.address, {}).get(data_type, None)
                # print("read cache: %s, %s" % (memory_type, address_object.address))

                if value is None:
                    value = func(address_object, *args, **kwargs)
                    AddressCacheSystem._cache.update({address_object.address: {data_type: value}})
                    # print("wrote cache: %s, %s" % (memory_type, address_object.address))
            except Exception:
                value = func(address_object, *args, **kwargs)
                warning("Can't Cache Address: %s" % address_object.address)
            return value
        return wrapper


    @classmethod
    def clear_cache(cls, target_address: int | None = None) -> None:
        if target_address is None: cls._cache.clear()
        else: cls._cache.pop(target_address)



class AddressMemoryRead(AddressCacheSystem):
    def __init__(self, address: int, process: ProcessAbs | None = None) -> None:
        self.address = address

        if process is None: process = Process.get_global_instance()
        if process is None: raise RuntimeError()
        self._process = process

    @AddressCacheSystem.caching_decorator
    def bytes(self, size) -> bytes | None: return self._process.memory_read.read_memory(self.address, size)

    @AddressCacheSystem.caching_decorator
    def bool(self) -> bool | None: return self._process.memory_read.read_bool(self.address)

    @AddressCacheSystem.caching_decorator
    def i8(self) -> int | None: return self._process.memory_read.read_i8(self.address)

    @AddressCacheSystem.caching_decorator
    def u8(self) -> int | None: return self._process.memory_read.read_i8(self.address)

    @AddressCacheSystem.caching_decorator
    def i16(self) -> int | None: return self._process.memory_read.read_i16(self.address)

    @AddressCacheSystem.caching_decorator
    def u16(self) -> int | None: return self._process.memory_read.read_u16(self.address)

    @AddressCacheSystem.caching_decorator
    def i32(self) -> int | None: return self._process.memory_read.read_i32(self.address)

    @AddressCacheSystem.caching_decorator
    def u32(self) -> int | None: return self._process.memory_read.read_u32(self.address)

    @AddressCacheSystem.caching_decorator
    def i64(self) -> int | None: return self._process.memory_read.read_i64(self.address)

    @AddressCacheSystem.caching_decorator
    def u64(self) -> int | None: return self._process.memory_read.read_u64(self.address)

    @AddressCacheSystem.caching_decorator
    def float(self) -> float | None: return self._process.memory_read.read_f32(self.address)

    @AddressCacheSystem.caching_decorator
    def vec(self, size: int) -> Sequence[float] | None: return self._process.memory_read.read_vec(self.address, size)

    @AddressCacheSystem.caching_decorator
    def vec2(self) -> Vec2 | None:
        vec = self._process.memory_read.read_vec(self.address, 2)
        if vec is None: return None

        return Vec2(*vec)

    @AddressCacheSystem.caching_decorator
    def vec3(self) -> Vec3 | None:
        vec = self._process.memory_read.read_vec(self.address, 3)
        if vec is None: return None

        return Vec3(*vec)

    @AddressCacheSystem.caching_decorator
    def str(self, size: int) -> str | None: return self._process.memory_read.read_str(self.address, size)


class Address(AddressMemoryRead):
    __slots__ = ("address", )

    def __init__(self, address: int, process: ProcessAbs | None = None) -> None:
        super().__init__(address, process)

    def __repr__(self) -> str:
        return "Address(%s | %s)" % (self.address, hex(self.address))

    def __eq__(self, other: int | Address) -> bool:
        if isinstance(other, int):
            return self.address == other
        if isinstance(other, Address):
            return self.address == other.address
        return False

    def __hash__(self) -> int:
        return hash((self.address, ))

    def __bool__(self) -> bool:
        return self.address != 0

    def __add__(self, other) -> Self:
        if isinstance(other, int):
            self.address += other
        if isinstance(other, Address):
            self.address += other.address
        return self

    def offset(self, value: int) -> Self:
        self.address += value
        return self

    def pointer(self) -> Self:
        self.address = self.u64()
        return self

    def pointer_chain(self, *offsets: int) -> Self | None:
        address = self.new()
        if address.address is None: return None

        for offset in offsets:
            if not isinstance(offset, int): raise ValueError()

            address = address.offset(offset).pointer()
            if address.address is None: return None

        return address

    def __copy__(self) -> Address:
        return Address(self.address)

    def new(self) -> Address:
        return self.__copy__()

    def copy(self):
        return self.__copy__()



