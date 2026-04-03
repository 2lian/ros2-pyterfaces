from __future__ import annotations

from typing import Any

import msgspec
import numpy as np
from cydr import types

from ..idl import JitStruct
from ..service_msgs.msg import ServiceEventInfo
from .msg import (
    ListParametersResult,
    LoggerLevel,
    Parameter,
    ParameterDescriptor,
    ParameterValue,
    SetLoggerLevelsResult,
    SetParametersResult,
)


class DescribeParameters_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/DescribeParameters_Request"
    names: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )


class DescribeParameters_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/DescribeParameters_Response"
    __unsupported_reason__ = (
        "descriptors is a collection of messages, which cydr does not support"
    )
    pass


class DescribeParameters(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/DescribeParameters"
    __unsupported_reason__ = (
        "response_message references unsupported message DescribeParameters_Response"
    )
    request_message: DescribeParameters_Request = msgspec.field(
        default_factory=DescribeParameters_Request
    )
    response_message: DescribeParameters_Response = msgspec.field(
        default_factory=DescribeParameters_Response
    )
    event_message: DescribeParameters_Event = msgspec.field(
        default_factory=lambda: DescribeParameters_Event()
    )


class DescribeParameters_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/DescribeParameters_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class GetLoggerLevels_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetLoggerLevels_Request"
    names: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )


class GetLoggerLevels_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetLoggerLevels_Response"
    __unsupported_reason__ = (
        "levels is a collection of messages, which cydr does not support"
    )
    pass


class GetLoggerLevels(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetLoggerLevels"
    __unsupported_reason__ = (
        "response_message references unsupported message GetLoggerLevels_Response"
    )
    request_message: GetLoggerLevels_Request = msgspec.field(
        default_factory=GetLoggerLevels_Request
    )
    response_message: GetLoggerLevels_Response = msgspec.field(
        default_factory=GetLoggerLevels_Response
    )
    event_message: GetLoggerLevels_Event = msgspec.field(
        default_factory=lambda: GetLoggerLevels_Event()
    )


class GetLoggerLevels_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetLoggerLevels_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class GetParameters_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameters_Request"
    names: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )


class GetParameters_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameters_Response"
    __unsupported_reason__ = (
        "values is a collection of messages, which cydr does not support"
    )
    pass


class GetParameters(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameters"
    __unsupported_reason__ = (
        "response_message references unsupported message GetParameters_Response"
    )
    request_message: GetParameters_Request = msgspec.field(
        default_factory=GetParameters_Request
    )
    response_message: GetParameters_Response = msgspec.field(
        default_factory=GetParameters_Response
    )
    event_message: GetParameters_Event = msgspec.field(
        default_factory=lambda: GetParameters_Event()
    )


class GetParameters_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameters_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class GetParameterTypes_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameterTypes_Request"
    names: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )


class GetParameterTypes_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameterTypes_Response"
    types: types.NDArray[Any, types.UInt8] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.uint8)
    )


class GetParameterTypes(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameterTypes"
    __unsupported_reason__ = (
        "event_message references unsupported message GetParameterTypes_Event"
    )
    request_message: GetParameterTypes_Request = msgspec.field(
        default_factory=GetParameterTypes_Request
    )
    response_message: GetParameterTypes_Response = msgspec.field(
        default_factory=GetParameterTypes_Response
    )
    event_message: GetParameterTypes_Event = msgspec.field(
        default_factory=lambda: GetParameterTypes_Event()
    )


class GetParameterTypes_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/GetParameterTypes_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class ListParameters_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/ListParameters_Request"
    prefixes: types.NDArray[Any, types.Bytes] = msgspec.field(
        default_factory=lambda: np.empty(0, dtype=np.bytes_)
    )
    depth: types.uint64 = np.uint64(0)


class ListParameters_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/ListParameters_Response"
    result: ListParametersResult = msgspec.field(default_factory=ListParametersResult)


class ListParameters(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/ListParameters"
    __unsupported_reason__ = (
        "event_message references unsupported message ListParameters_Event"
    )
    request_message: ListParameters_Request = msgspec.field(
        default_factory=ListParameters_Request
    )
    response_message: ListParameters_Response = msgspec.field(
        default_factory=ListParameters_Response
    )
    event_message: ListParameters_Event = msgspec.field(
        default_factory=lambda: ListParameters_Event()
    )


class ListParameters_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/ListParameters_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class SetLoggerLevels_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetLoggerLevels_Request"
    __unsupported_reason__ = (
        "levels is a collection of messages, which cydr does not support"
    )
    pass


class SetLoggerLevels_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetLoggerLevels_Response"
    __unsupported_reason__ = (
        "results is a collection of messages, which cydr does not support"
    )
    pass


class SetLoggerLevels(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetLoggerLevels"
    __unsupported_reason__ = (
        "request_message references unsupported message SetLoggerLevels_Request"
    )
    request_message: SetLoggerLevels_Request = msgspec.field(
        default_factory=SetLoggerLevels_Request
    )
    response_message: SetLoggerLevels_Response = msgspec.field(
        default_factory=SetLoggerLevels_Response
    )
    event_message: SetLoggerLevels_Event = msgspec.field(
        default_factory=lambda: SetLoggerLevels_Event()
    )


class SetLoggerLevels_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetLoggerLevels_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class SetParametersAtomically_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParametersAtomically_Request"
    __unsupported_reason__ = (
        "parameters is a collection of messages, which cydr does not support"
    )
    pass


class SetParametersAtomically_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParametersAtomically_Response"
    result: SetParametersResult = msgspec.field(default_factory=SetParametersResult)


class SetParametersAtomically(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParametersAtomically"
    __unsupported_reason__ = (
        "request_message references unsupported message SetParametersAtomically_Request"
    )
    request_message: SetParametersAtomically_Request = msgspec.field(
        default_factory=SetParametersAtomically_Request
    )
    response_message: SetParametersAtomically_Response = msgspec.field(
        default_factory=SetParametersAtomically_Response
    )
    event_message: SetParametersAtomically_Event = msgspec.field(
        default_factory=lambda: SetParametersAtomically_Event()
    )


class SetParametersAtomically_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParametersAtomically_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass


class SetParameters_Request(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParameters_Request"
    __unsupported_reason__ = (
        "parameters is a collection of messages, which cydr does not support"
    )
    pass


class SetParameters_Response(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParameters_Response"
    __unsupported_reason__ = (
        "results is a collection of messages, which cydr does not support"
    )
    pass


class SetParameters(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParameters"
    __unsupported_reason__ = (
        "request_message references unsupported message SetParameters_Request"
    )
    request_message: SetParameters_Request = msgspec.field(
        default_factory=SetParameters_Request
    )
    response_message: SetParameters_Response = msgspec.field(
        default_factory=SetParameters_Response
    )
    event_message: SetParameters_Event = msgspec.field(
        default_factory=lambda: SetParameters_Event()
    )


class SetParameters_Event(JitStruct):
    __idl_typename__ = "rcl_interfaces/srv/SetParameters_Event"
    __unsupported_reason__ = (
        "request is a collection of messages, which cydr does not support"
    )
    pass
