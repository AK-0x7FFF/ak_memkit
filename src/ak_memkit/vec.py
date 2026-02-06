from __future__ import annotations

from functools import wraps
from typing import Sequence, Self, Callable, TypeVar, Union

import numpy as np
from numba import njit

_T = TypeVar("_T")


class Vec2:
    __slots__ = ("array",)

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.array = np.array((x, y), dtype=np.float32)

    @classmethod
    def from_sequence(cls, v: Sequence[int | float]) -> Self:
        return cls(v[0], v[1])

    @classmethod
    def from_dict(cls, d: dict[str, int | float]) -> Self:
        return cls(d.get("x", 0.0), d.get("y", 0.0))

    def __copy__(self) -> Self:
        return Vec2(self.array[0], self.array[1])

    def new(self) -> Self:
        return self.__copy__()

    def copy(self) -> Self:
        return self.__copy__()

    @property
    def x(self) -> float:
        return self.array[0]

    @x.setter
    def x(self, value: float) -> None:
        self.array[0] = value

    @property
    def y(self) -> float:
        return self.array[1]

    @y.setter
    def y(self, value: float) -> None:
        self.array[1] = value

    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, int):
            # lise like
            return self.array[index]
        if isinstance(index, str):
            # dict like
            if index == "x": return self.array[0]
            if index == "y": return self.array[1]
        raise TypeError("index must be int or str")

    def __repr__(self) -> str:
        return f"Vec2({self.array[0]}, {self.array[1]})"

    def to_sequence(self) -> list:
        return [self.array[0], self.array[1]]

    def to_dict(self) -> dict[str, float]:
        return {"x": self.array[0], "y": self.array[1]}

    _TH = Union["Vec2", float | np.dtype[np.float32]]

    @staticmethod
    def __argument_check(to_vec: bool) -> Callable[[Callable[[Vec2], Vec2]], Callable[[Vec2], Vec2]]:
        def decorator(func: _T) -> _T:
            @wraps(func)
            def wrapper(self, other: Vec2._TH) -> float | Vec2:
                if isinstance(other, float):
                    other = np.array((other, other), dtype=np.float32)
                elif isinstance(other, Vec2):
                    other = other.array

                return func(self.array, other) if not to_vec else Vec2.from_sequence(func(self.array, other))

            return wrapper

        return decorator

    @__argument_check(True)
    @njit
    def __add__(self: np.dtype[np.float32], other: Vec2._TH) -> Vec2:
        return self + other

    @__argument_check(True)
    @njit
    def __sub__(self: np.dtype[np.float32], other: Vec2._TH) -> Vec2:
        return self - other

    @__argument_check(False)
    @njit
    def distance(self: np.dtype[np.float32], other: Vec2._TH) -> float:
        return np.linalg.norm(self - other)

    @__argument_check(False)
    @njit
    def angle(self: np.dtype[np.float32], other: Vec2._TH) -> float:
        angle_rad = np.arctan2(other[1], other[0]) - np.arctan2(self[1], self[0])
        return np.degrees(angle_rad)

    @__argument_check(True)
    @njit
    def min(self: np.dtype[np.float32], other: Vec2._TH) -> Vec2:
        return np.array((
            min(self[0], other[0]),
            min(self[1], other[1])
        ), dtype=np.float32)

    @__argument_check(True)
    @njit
    def max(self: np.dtype[np.float32], other: Vec2._TH) -> Vec2:
        return np.array((
            max(self[0], other[0]),
            max(self[1], other[1])
        ), dtype=np.float32)


class Vec3:
    __slots__ = ("array",)

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.array = np.array((x, y, z), dtype=np.float32)

    @classmethod
    def from_sequence(cls, v: Sequence[int | float]) -> Self:
        return cls(v[0], v[1], v[2])

    @classmethod
    def from_dict(cls, d: dict[str, int | float]) -> Self:
        return cls(d.get("x", 0.0), d.get("y", 0.0), d.get("z", 0.0))


    def __copy__(self) -> Self:
        return Vec3(self.array[0], self.array[1], self.array[2])

    def new(self) -> Self:
        return self.__copy__()

    def copy(self) -> Self:
        return self.__copy__()

    @property
    def x(self) -> float:
        return self.array[0]

    @x.setter
    def x(self, value: float) -> None:
        self.array[0] = value

    @property
    def y(self) -> float:
        return self.array[1]

    @y.setter
    def y(self, value: float) -> None:
        self.array[1] = value

    @property
    def z(self) -> float:
        return self.array[2]

    @z.setter
    def z(self, value: float) -> None:
        self.array[2] = value

    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, int):
            # lise like
            return self.array[index]
        if isinstance(index, str):
            # dict like
            if index == "x": return self.array[0]
            if index == "y": return self.array[1]
            if index == "z": return self.array[2]
        raise TypeError("index must be int or str")

    def __repr__(self) -> str:
        return f"Vec3({self.array[0]}, {self.array[1]}, {self.array[2]})"

    def to_sequence(self) -> list:
        return [self.array[0], self.array[1], self.array[2]]

    def to_dict(self) -> dict[str, float]:
        return {"x": self.array[0], "y": self.array[1], "z": self.array[2]}

    _TH = Union["Vec3", float | np.dtype[np.float32]]

    @staticmethod
    def __argument_check(cast: bool) -> Callable[[Callable[[Vec3], Vec3]], Callable[[Vec3], Vec3]]:
        def decorator(func: _T) -> _T:
            @wraps(func)
            def wrapper(self, other: Vec3._TH) -> float | Vec3:
                if isinstance(other, float):
                    other = np.array((other, other), dtype=np.float32)
                elif isinstance(other, Vec3):
                    other = other.array

                return func(self.array, other) if not cast else Vec3.from_sequence(func(self.array, other))

            return wrapper

        return decorator

    @__argument_check(True)
    @njit
    def __add__(self: np.dtype[np.float32], other: Vec3._TH) -> Vec3:
        return self + other

    @__argument_check(True)
    @njit
    def __sub__(self: np.dtype[np.float32], other: Vec3._TH) -> Vec3:
        return self - other

    @__argument_check(False)
    @njit
    def distance(self: np.dtype[np.float32], b: Vec3._TH) -> float:
        return np.sqrt(np.sum((self - b) ** 2))

    @__argument_check(True)
    @njit
    def cross(self: np.dtype[np.float32], b: Vec3._TH) -> Vec3:
        x = self[1] * b[2] - self[2] * b[1]
        y = self[2] * b[0] - self[0] * b[2]
        z = self[0] * b[1] - self[1] * b[0]

        return np.array([x, y, z])

    @__argument_check(False)
    @njit
    def dot(self: np.dtype[np.float32], b: Vec3._TH) -> float:
        return np.dot(self, b)

    @__argument_check(True)
    @njit
    def min(self: np.dtype[np.float32], other: Vec3._TH) -> Vec3:
        return np.array((
            min(self[0], other[0]),
            min(self[1], other[1]),
            min(self[2], other[2])
        ), dtype=np.float32)

    @__argument_check(True)
    @njit
    def max(self: np.dtype[np.float32], other: Vec3._TH) -> Vec3:
        return np.array((
            max(self[0], other[0]),
            max(self[1], other[1]),
            max(self[2], other[2])
        ), dtype=np.float32)


if __name__ == '__main__':
    from timeit import timeit

    a = Vec3(12323, 45656)
    b = Vec3(453335, -986366)

    print(a.dot(b), a.dot(b))
    print(timeit(lambda: a.dot(b)))
    # print(timeit(lambda: a._dot(b)))