from __future__ import annotations

from functools import wraps
from typing import Sequence, Self, Callable, TypeVar

import numpy as np
from numba import njit


_T = TypeVar("_T")


class Vec2:
    __slots__ = ("_array", )

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self._array = np.array((x, y), dtype=np.float32)

    @classmethod
    def from_sequence(cls, v: Sequence[int | float]) -> Self:
        return cls(v[0], v[1])

    @classmethod
    def from_dict(cls, d: dict[str, int | float]) -> Self:
        return cls(d.get("x", 0.0), d.get("y", 0.0))

    @classmethod
    def empty(cls) -> Self:
        return cls()

    def __copy__(self) -> Self:
        return Vec2(self._array[0], self._array[1])

    def new(self) -> Self:
        self.__copy__()

    def copy(self) -> Self:
        self.__copy__()

    @property
    def x(self) -> float:
        return self._array[0]

    @property
    def y(self) -> float:
        return self._array[1]

    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, int):
            # lise like
            return self._array[index]
        if isinstance(index, str):
            # dict like
            if index == "x": return self._array[0]
            if index == "y": return self._array[1]
        raise TypeError("index must be int or str")

    def __repr__(self) -> str:
        return f"Vec2({self._array[0]}, {self._array[1]})"

    @staticmethod
    def __argument_check(to_vec: bool) -> Callable[[Callable[[Vec2], Vec2]], Callable[[Vec2], Vec2]]:
        def decorator(func: _T) -> _T:
            @wraps(func)
            def wrapper(self, other: Vec2 | np.dtype[np.float32]) -> float | Vec2:
                if isinstance(other, Vec2):
                    other = other._array

                return func(self._array, other) if not to_vec else Vec2.from_sequence(func(self._array, other))

            return wrapper
        return decorator

    @__argument_check(False)
    @njit
    def distance(self: np.dtype[np.float32], other: Vec2 | np.dtype[np.float32]) -> float:
        return np.linalg.norm(self - other)


    @__argument_check(False)
    @njit
    def angle(self: np.dtype[np.float32], other: Vec2 | np.dtype[np.float32]) -> float:
        angle_rad = np.arctan2(other[1], other[0]) - np.arctan2(self[1], self[0])
        return np.degrees(angle_rad)


class Vec3:
    __slots__ = ("_array", )

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float =0.0) -> None:
        self._array = np.array((x, y, z), dtype=np.float32)

    @classmethod
    def from_sequence(cls, v: Sequence[int | float]) -> Self:
        return cls(v[0], v[1], v[2])

    @classmethod
    def from_dict(cls, d: dict[str, int | float]) -> Self:
        return cls(d.get("x", 0.0), d.get("y", 0.0), d.get("z", 0.0))

    @classmethod
    def empty(cls) -> Self:
        return cls()

    def __copy__(self) -> Self:
        return Vec3(self._array[0], self._array[1], self._array[2])

    def new(self) -> Self:
        self.__copy__()

    def copy(self) -> Self:
        self.__copy__()

    @property
    def x(self) -> float:
        return self._array[0]

    @property
    def y(self) -> float:
        return self._array[1]

    @property
    def z(self) -> float:
        return self._array[2]

    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, int):
            # lise like
            return self._array[index]
        if isinstance(index, str):
            # dict like
            if index == "x": return self._array[0]
            if index == "y": return self._array[1]
            if index == "z": return self._array[2]
        raise TypeError("index must be int or str")

    def __repr__(self) -> str:
        return f"Vec3({self._array[0]}, {self._array[1]}, {self._array[2]})"


    @staticmethod
    def __argument_check(cast: bool) -> Callable[[Callable[[Vec3], Vec3]], Callable[[Vec3], Vec3]]:
        def decorator(func: _T) -> _T:
            @wraps(func)
            def wrapper(self, other: Vec3 | np.dtype[np.float32]) -> float | Vec3:
                if isinstance(other, Vec3):
                    other = other._array

                return func(self._array, other) if not cast else Vec3.from_sequence(func(self._array, other))

            return wrapper
        return decorator

    @__argument_check(False)
    @njit
    def distance(self: np.dtype[np.float32], b: Vec3 | np.dtype[np.float32]) -> float:
        return np.sqrt(np.sum((self - b) ** 2))

    @__argument_check(True)
    @njit
    def cross(self: np.dtype[np.float32], b: Vec3 | np.dtype[np.float32]) -> Vec3:
        x = self[1] * b[2] - self[2] * b[1]
        y = self[2] * b[0] - self[0] * b[2]
        z = self[0] * b[1] - self[1] * b[0]

        return np.array([x, y, z])

    @__argument_check(False)
    @njit
    def dot(self: np.dtype[np.float32], b: Vec3 | np.dtype[np.float32]) -> float:
        return np.dot(self, b)

if __name__ == '__main__':
    from timeit import timeit
    a = Vec3(12323, 45656)
    b = Vec3(453335, -986366)

    print(a.dot(b), a.dot(b))
    print(timeit(lambda: a.dot(b)))
    # print(timeit(lambda: a._dot(b)))
