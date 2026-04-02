from dataclasses import dataclass, field
from typing import ClassVar, Literal

from ..builtin_interfaces.msg import Time
from ..idl import IdlStruct, types


@dataclass
class FloatingPointRange(IdlStruct, typename="rcl_interfaces/msg/FloatingPointRange"):
    from_value: types.float64 = 0.0
    to_value: types.float64 = 0.0
    step: types.float64 = 0.0


@dataclass
class IntegerRange(IdlStruct, typename="rcl_interfaces/msg/IntegerRange"):
    from_value: types.int64 = 0
    to_value: types.int64 = 0
    step: types.uint64 = 0


@dataclass
class ListParametersResult(IdlStruct, typename="rcl_interfaces/msg/ListParametersResult"):
    names: types.sequence[str] = field(default_factory=list)
    prefixes: types.sequence[str] = field(default_factory=list)


@dataclass
class LoggerLevel(IdlStruct, typename="rcl_interfaces/msg/LoggerLevel"):
    LOG_LEVEL_UNKNOWN: ClassVar[Literal[0]] = 0
    LOG_LEVEL_DEBUG: ClassVar[Literal[10]] = 10
    LOG_LEVEL_INFO: ClassVar[Literal[20]] = 20
    LOG_LEVEL_WARN: ClassVar[Literal[30]] = 30
    LOG_LEVEL_ERROR: ClassVar[Literal[40]] = 40
    LOG_LEVEL_FATAL: ClassVar[Literal[50]] = 50

    name: str = ""
    level: types.uint32 = 0


@dataclass
class Log(IdlStruct, typename="rcl_interfaces/msg/Log"):
    DEBUG: ClassVar[Literal[10]] = 10
    INFO: ClassVar[Literal[20]] = 20
    WARN: ClassVar[Literal[30]] = 30
    ERROR: ClassVar[Literal[40]] = 40
    FATAL: ClassVar[Literal[50]] = 50

    stamp: Time = field(default_factory=Time)
    level: types.uint8 = 0
    name: str = ""
    msg: str = ""
    file: str = ""
    function: str = ""
    line: types.uint32 = 0


@dataclass
class ParameterType(IdlStruct, typename="rcl_interfaces/msg/ParameterType"):
    PARAMETER_NOT_SET: ClassVar[Literal[0]] = 0
    PARAMETER_BOOL: ClassVar[Literal[1]] = 1
    PARAMETER_INTEGER: ClassVar[Literal[2]] = 2
    PARAMETER_DOUBLE: ClassVar[Literal[3]] = 3
    PARAMETER_STRING: ClassVar[Literal[4]] = 4
    PARAMETER_BYTE_ARRAY: ClassVar[Literal[5]] = 5
    PARAMETER_BOOL_ARRAY: ClassVar[Literal[6]] = 6
    PARAMETER_INTEGER_ARRAY: ClassVar[Literal[7]] = 7
    PARAMETER_DOUBLE_ARRAY: ClassVar[Literal[8]] = 8
    PARAMETER_STRING_ARRAY: ClassVar[Literal[9]] = 9


@dataclass
class ParameterValue(IdlStruct, typename="rcl_interfaces/msg/ParameterValue"):
    type: types.uint8 = 0
    bool_value: bool = False
    integer_value: types.int64 = 0
    double_value: types.float64 = 0.0
    string_value: str = ""
    byte_array_value: types.sequence[types.byte] = field(default_factory=list)
    bool_array_value: types.sequence[bool] = field(default_factory=list)
    integer_array_value: types.sequence[types.int64] = field(default_factory=list)
    double_array_value: types.sequence[types.float64] = field(default_factory=list)
    string_array_value: types.sequence[str] = field(default_factory=list)


@dataclass
class SetLoggerLevelsResult(
    IdlStruct, typename="rcl_interfaces/msg/SetLoggerLevelsResult"
):
    successful: bool = False
    reason: str = ""


@dataclass
class SetParametersResult(IdlStruct, typename="rcl_interfaces/msg/SetParametersResult"):
    successful: bool = False
    reason: str = ""


@dataclass
class ParameterDescriptor(IdlStruct, typename="rcl_interfaces/msg/ParameterDescriptor"):
    name: str = ""
    type: types.uint8 = 0
    description: str = ""
    additional_constraints: str = ""
    read_only: bool = False
    dynamic_typing: bool = False
    floating_point_range: types.sequence[FloatingPointRange, 1] = field(
        default_factory=list
    )
    integer_range: types.sequence[IntegerRange, 1] = field(default_factory=list)


@dataclass
class Parameter(IdlStruct, typename="rcl_interfaces/msg/Parameter"):
    name: str = ""
    value: ParameterValue = field(default_factory=ParameterValue)


@dataclass
class ParameterEventDescriptors(
    IdlStruct, typename="rcl_interfaces/msg/ParameterEventDescriptors"
):
    new_parameters: types.sequence[ParameterDescriptor] = field(default_factory=list)
    changed_parameters: types.sequence[ParameterDescriptor] = field(default_factory=list)
    deleted_parameters: types.sequence[ParameterDescriptor] = field(default_factory=list)


@dataclass
class ParameterEvent(IdlStruct, typename="rcl_interfaces/msg/ParameterEvent"):
    stamp: Time = field(default_factory=Time)
    node: str = ""
    new_parameters: types.sequence[Parameter] = field(default_factory=list)
    changed_parameters: types.sequence[Parameter] = field(default_factory=list)
    deleted_parameters: types.sequence[Parameter] = field(default_factory=list)
