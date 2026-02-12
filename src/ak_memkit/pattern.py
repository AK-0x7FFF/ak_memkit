from re import search, DOTALL
from typing import Self, Any

from .memory.process import Process
from .memory.abstract_classes import MemoryReadAbs, ModuleAbs
from .address import Address


class Pattern:
    def __init__(self, pattern: str, buffer: bytes | bytearray | memoryview | None = None):
        self.pattern = pattern
        self.buffer = buffer

        self._pattern_offset: int | None = None

    def __repr__(self) -> str:
        return "Pattern(\"%s\", %s)" % (self.pattern, self.offset)

    # @property
    # def address(self) -> int:
    #     return self._module_base + self._pattern_offset
    #
    # def to_address(self) -> Address:
    #     return Address(self._module_base + self._pattern_offset)

    @property
    def offset(self) -> int:
        return self._pattern_offset

    @staticmethod
    def pattern_str_to_regex_bytes(pattern: str) -> bytes:
        return rb"".join([
            rb"." if "?" in hex_byte else rb"\x" + hex_byte.encode("utf-8")
            for hex_byte in pattern.split(" ")
        ])

    def aob_scan(self, auto_trans_2_regex: bool = True) -> Self:
        try:
            if auto_trans_2_regex: pattern_match_bytes = self.pattern_str_to_regex_bytes(self.pattern)
            else: pattern_match_bytes = self.pattern
            match_offset = search(pattern_match_bytes, self.buffer, DOTALL)

            if match_offset is None:
                # raise PatternConvertError(self.pattern, pattern_match_bytes)
                raise RuntimeError()
            self._pattern_offset = match_offset.start()
            return self
        except Exception as err:
            # raise PatternConvertError(self.pattern, err)
            raise RuntimeError() from err


    def pattern_bytes(self, offset: int, size: int) -> bytes | bytearray | memoryview:
        return self.buffer[self._pattern_offset + offset:self._pattern_offset + offset + size]


    def add(self, value: int) -> Self:
        self._pattern_offset += value
        return self

    def rip(self, offset: int = 3, length: int = 7) -> Self:
        self._pattern_offset = self._pattern_offset + MemoryReadAbs.unpack_byte(self.pattern_bytes(offset, 4), "I") + length
        return self

    def slice(self, start: int, end: int) -> Self:
        byte = self.pattern_bytes(start, end - start)
        self._pattern_offset = int.from_bytes(byte, "little")

        return self

    # def update_module_base(self, module_base: int) -> Self:
    #     self._module_base = module_base
    #     return self