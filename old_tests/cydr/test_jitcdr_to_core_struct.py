from typing import Any, ClassVar, Literal

import msgspec
import numpy as np
import pytest
from nptyping import Bytes, Float64, NDArray, Shape, UInt8

pytest.importorskip("cydr")

from ros2_pyterfaces.idl import IdlStruct as CoreStruct
from ros2_pyterfaces.idl_types import types
from ros2_pyterfaces.jitcdr.converter import to_core_struct
from ros2_pyterfaces.jitcdr.idl import JitStruct, idl
from ros2_pyterfaces.utils.idl import message_field_annotations


class Time(JitStruct):
    __idl_typename__: ClassVar[Literal["builtin_interfaces/msg/Time"]] = (
        "builtin_interfaces/msg/Time"
    )
    sec: idl.int32 = idl.int32(1)
    nanosec: idl.uint32 = idl.uint32(2)


class Example(JitStruct):
    __idl_typename__: ClassVar[Literal["pkg/msg/Example"]] = "pkg/msg/Example"
    stamp: Time = msgspec.field(default_factory=Time)
    frame_id: idl.string = b"map"
    values: NDArray[Any, Float64] = msgspec.field(
        default_factory=lambda: np.array([1.5, 2.5], dtype=np.float64)
    )
    names: NDArray[Any, Bytes] = msgspec.field(
        default_factory=lambda: np.array([b"a", b"b"], dtype=np.bytes_)
    )
    gid: NDArray[Shape["4"], UInt8] = msgspec.field(
        default_factory=lambda: np.array([1, 2, 3, 4], dtype=np.uint8)
    )


def test_to_core_struct_converts_jit_class_annotations():
    core_time = to_core_struct(Time)
    core_example = to_core_struct(Example)
    hints = message_field_annotations(core_example, include_extras=True)

    assert issubclass(core_example, CoreStruct)
    assert core_example is to_core_struct(Example)
    assert core_example.__idl_typename__ == "pkg/msg/Example"
    assert hints["stamp"] is core_time
    assert hints["frame_id"] is str
    assert hints["values"] == types.sequence[types.float64]
    assert hints["names"] == types.sequence[str]
    assert hints["gid"] == types.array[types.uint8, 4]


def test_to_core_struct_converts_jit_instance_values():
    core_example = to_core_struct(Example())
    core_time = to_core_struct(Time)

    assert isinstance(core_example, to_core_struct(Example))
    assert isinstance(core_example.stamp, core_time)
    assert core_example.stamp.sec == 1
    assert core_example.stamp.nanosec == 2
    assert core_example.frame_id == "map"
    assert core_example.values == [1.5, 2.5]
    assert core_example.names == ["a", "b"]
    assert core_example.gid == bytes([1, 2, 3, 4])
