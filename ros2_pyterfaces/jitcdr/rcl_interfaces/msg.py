from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..builtin_interfaces.msg import Time

class FloatingPointRange(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/FloatingPointRange'
    from_value: types.float64 = np.float64(0.0)
    to_value: types.float64 = np.float64(0.0)
    step: types.float64 = np.float64(0.0)

class IntegerRange(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/IntegerRange'
    from_value: types.int64 = np.int64(0)
    to_value: types.int64 = np.int64(0)
    step: types.uint64 = np.uint64(0)

class ListParametersResult(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ListParametersResult'
    names: types.NDArray[Any, types.Bytes] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.bytes_))
    prefixes: types.NDArray[Any, types.Bytes] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.bytes_))

class LoggerLevel(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/LoggerLevel'
    name: types.string = b''
    level: types.uint32 = np.uint32(0)

class Log(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/Log'
    stamp: Time = msgspec.field(default_factory=Time)
    level: types.uint8 = np.uint8(0)
    name: types.string = b''
    msg: types.string = b''
    file: types.string = b''
    function: types.string = b''
    line: types.uint32 = np.uint32(0)

class ParameterType(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ParameterType'

class ParameterValue(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ParameterValue'
    type: types.uint8 = np.uint8(0)
    bool_value: types.boolean = False
    integer_value: types.int64 = np.int64(0)
    double_value: types.float64 = np.float64(0.0)
    string_value: types.string = b''
    byte_array_value: types.NDArray[Any, types.UInt8] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.uint8))
    bool_array_value: types.NDArray[Any, types.Bool] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.bool_))
    integer_array_value: types.NDArray[Any, types.Int64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.int64))
    double_array_value: types.NDArray[Any, types.Float64] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.float64))
    string_array_value: types.NDArray[Any, types.Bytes] = msgspec.field(default_factory=lambda: np.empty(0, dtype=np.bytes_))

class SetLoggerLevelsResult(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/SetLoggerLevelsResult'
    successful: types.boolean = False
    reason: types.string = b''

class SetParametersResult(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/SetParametersResult'
    successful: types.boolean = False
    reason: types.string = b''

class ParameterDescriptor(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ParameterDescriptor'
    __unsupported_reason__ = 'floating_point_range is a collection of messages, which cydr does not support'
    pass

class Parameter(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/Parameter'
    name: types.string = b''
    value: ParameterValue = msgspec.field(default_factory=ParameterValue)

class ParameterEventDescriptors(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ParameterEventDescriptors'
    __unsupported_reason__ = 'new_parameters is a collection of messages, which cydr does not support'
    pass

class ParameterEvent(JitStruct):
    __idl_typename__ = 'rcl_interfaces/msg/ParameterEvent'
    __unsupported_reason__ = 'new_parameters is a collection of messages, which cydr does not support'
    pass
