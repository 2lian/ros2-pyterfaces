from dataclasses import dataclass, field
from typing import ClassVar, Literal

from .. import idl
from .msg import (
    ListParametersResult,
    LoggerLevel,
    Parameter,
    ParameterDescriptor,
    ParameterValue,
    SetLoggerLevelsResult,
    SetParametersResult,
)


@dataclass
class DescribeParameters_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/DescribeParameters_Request"
):
    names: idl.types.sequence[str] = field(default_factory=list)


@dataclass
class DescribeParameters_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/DescribeParameters_Response"
):
    descriptors: idl.types.sequence[ParameterDescriptor] = field(default_factory=list)


DescribeParameters = idl.make_idl_service(
    DescribeParameters_Request, DescribeParameters_Response
)
DescribeParameters_Event = DescribeParameters.Event


@dataclass
class GetLoggerLevels_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetLoggerLevels_Request"
):
    names: idl.types.sequence[str] = field(default_factory=list)


@dataclass
class GetLoggerLevels_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetLoggerLevels_Response"
):
    levels: idl.types.sequence[LoggerLevel] = field(default_factory=list)


GetLoggerLevels = idl.make_idl_service(GetLoggerLevels_Request, GetLoggerLevels_Response)
GetLoggerLevels_Event = GetLoggerLevels.Event


@dataclass
class GetParameters_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetParameters_Request"
):
    names: idl.types.sequence[str] = field(default_factory=list)


@dataclass
class GetParameters_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetParameters_Response"
):
    values: idl.types.sequence[ParameterValue] = field(default_factory=list)


GetParameters = idl.make_idl_service(GetParameters_Request, GetParameters_Response)
GetParameters_Event = GetParameters.Event


@dataclass
class GetParameterTypes_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetParameterTypes_Request"
):
    names: idl.types.sequence[str] = field(default_factory=list)


@dataclass
class GetParameterTypes_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/GetParameterTypes_Response"
):
    types: idl.types.sequence[idl.types.uint8] = field(default_factory=list)


GetParameterTypes = idl.make_idl_service(
    GetParameterTypes_Request, GetParameterTypes_Response
)
GetParameterTypes_Event = GetParameterTypes.Event


@dataclass
class ListParameters_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/ListParameters_Request"
):
    DEPTH_RECURSIVE: ClassVar[Literal[0]] = 0

    prefixes: idl.types.sequence[str] = field(default_factory=list)
    depth: idl.types.uint64 = 0


@dataclass
class ListParameters_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/ListParameters_Response"
):
    result: ListParametersResult = field(default_factory=ListParametersResult)


ListParameters = idl.make_idl_service(ListParameters_Request, ListParameters_Response)
ListParameters_Event = ListParameters.Event


@dataclass
class SetLoggerLevels_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetLoggerLevels_Request"
):
    levels: idl.types.sequence[LoggerLevel] = field(default_factory=list)


@dataclass
class SetLoggerLevels_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetLoggerLevels_Response"
):
    results: idl.types.sequence[SetLoggerLevelsResult] = field(default_factory=list)


SetLoggerLevels = idl.make_idl_service(
    SetLoggerLevels_Request, SetLoggerLevels_Response
)
SetLoggerLevels_Event = SetLoggerLevels.Event


@dataclass
class SetParametersAtomically_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetParametersAtomically_Request"
):
    parameters: idl.types.sequence[Parameter] = field(default_factory=list)


@dataclass
class SetParametersAtomically_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetParametersAtomically_Response"
):
    result: SetParametersResult = field(default_factory=SetParametersResult)


SetParametersAtomically = idl.make_idl_service(
    SetParametersAtomically_Request, SetParametersAtomically_Response
)
SetParametersAtomically_Event = SetParametersAtomically.Event


@dataclass
class SetParameters_Request(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetParameters_Request"
):
    parameters: idl.types.sequence[Parameter] = field(default_factory=list)


@dataclass
class SetParameters_Response(
    idl.IdlStruct, typename="rcl_interfaces/srv/SetParameters_Response"
):
    results: idl.types.sequence[SetParametersResult] = field(default_factory=list)


SetParameters = idl.make_idl_service(SetParameters_Request, SetParameters_Response)
SetParameters_Event = SetParameters.Event
