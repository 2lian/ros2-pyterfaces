from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import IdlStruct
from ..builtin_interfaces.msg import Time

class Bool(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Bool'
    data: types.boolean = False

class Byte(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Byte'
    data: types.byte = np.uint8(0)

class Char(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Char'
    data: types.uint8 = np.uint8(0)

class ColorRGBA(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/ColorRGBA'
    r: types.float32 = np.float32(0.0)
    g: types.float32 = np.float32(0.0)
    b: types.float32 = np.float32(0.0)
    a: types.float32 = np.float32(0.0)

class Empty(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Empty'

class Float32(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Float32'
    data: types.float32 = np.float32(0.0)

class Float64(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Float64'
    data: types.float64 = np.float64(0.0)

class Header(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Header'
    stamp: Time = msgspec.field(default_factory=Time)
    frame_id: types.string = b''

class Int16(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int16'
    data: types.int16 = np.int16(0)

class Int32(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int32'
    data: types.int32 = np.int32(0)

class Int64(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int64'
    data: types.int64 = np.int64(0)

class Int8(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int8'
    data: types.int8 = np.int8(0)

class MultiArrayDimension(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/MultiArrayDimension'
    label: types.string = b''
    size: types.uint32 = np.uint32(0)
    stride: types.uint32 = np.uint32(0)

class String(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/String'
    data: types.string = b''

class UInt16(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt16'
    data: types.uint16 = np.uint16(0)

class UInt32(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt32'
    data: types.uint32 = np.uint32(0)

class UInt64(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt64'
    data: types.uint64 = np.uint64(0)

class UInt8(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt8'
    data: types.uint8 = np.uint8(0)

class MultiArrayLayout(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/MultiArrayLayout'
    __unsupported_reason__ = 'dim is a collection of messages, which cydr does not support'
    pass

class ByteMultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/ByteMultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.UInt8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint8))

class Float32MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Float32MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Float32] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float32))

class Float64MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Float64MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))

class Int16MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int16MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Int16] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int16))

class Int32MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int32MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Int32] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int32))

class Int64MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int64MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Int64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int64))

class Int8MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/Int8MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.Int8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int8))

class UInt16MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt16MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.UInt16] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint16))

class UInt32MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt32MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.UInt32] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint32))

class UInt64MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt64MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.UInt64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint64))

class UInt8MultiArray(IdlStruct):
    __idl_typename__ = 'std_msgs/msg/UInt8MultiArray'
    __unsupported_reason__ = 'layout references unsupported message MultiArrayLayout'
    layout: MultiArrayLayout = msgspec.field(default_factory=MultiArrayLayout)
    data: types.NDArray[Any, types.UInt8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint8))
