from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any


@dataclass(frozen=True)
class sequence:
    subtype: Any
    max_length: int | None = None

    def __class_getitem__(cls, params: Any) -> Any:
        if not isinstance(params, tuple):
            subtype = params
            max_length = None
        elif len(params) == 1:
            subtype = params[0]
            max_length = None
        elif len(params) == 2:
            subtype, max_length = params
        else:
            raise TypeError("sequence[...] expects subtype or (subtype, max_length)")
        return Annotated[list[subtype], cls(subtype, max_length)]


@dataclass(frozen=True)
class array:
    subtype: Any
    length: int

    def __class_getitem__(cls, params: Any) -> Any:
        if not isinstance(params, tuple) or len(params) != 2:
            raise TypeError("array[...] expects (subtype, length)")
        subtype, length = params
        return Annotated[list[subtype], cls(subtype, int(length))]


@dataclass(frozen=True)
class bounded_str:
    max_length: int

    def __class_getitem__(cls, max_length: Any) -> Any:
        return Annotated[str, cls(int(max_length))]


@dataclass(frozen=True)
class typedef:
    subtype: Any

    def __class_getitem__(cls, subtype: Any) -> Any:
        return Annotated[subtype, cls(subtype)]


class _Types:
    bool = Annotated[bool, "bool"]
    byte = Annotated[int, "byte"]
    char = Annotated[int, "char"]
    int8 = Annotated[int, "int8"]
    uint8 = Annotated[int, "uint8"]
    int16 = Annotated[int, "int16"]
    uint16 = Annotated[int, "uint16"]
    int32 = Annotated[int, "int32"]
    uint32 = Annotated[int, "uint32"]
    int64 = Annotated[int, "int64"]
    uint64 = Annotated[int, "uint64"]
    float32 = Annotated[float, "float32"]
    float64 = Annotated[float, "float64"]

    sequence = sequence
    array = array
    bounded_str = bounded_str
    typedef = typedef


types = _Types()
