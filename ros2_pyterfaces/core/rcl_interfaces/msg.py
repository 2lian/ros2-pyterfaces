from .. import Array, BoundedString, CoreSchema, Sequence

from ..builtin_interfaces.msg import Time

FloatingPointRange: CoreSchema = {
    "__typename": "rcl_interfaces/msg/FloatingPointRange",
    "from_value": "float64",
    "to_value": "float64",
    "step": "float64",
}

IntegerRange: CoreSchema = {
    "__typename": "rcl_interfaces/msg/IntegerRange",
    "from_value": "int64",
    "to_value": "int64",
    "step": "uint64",
}

ListParametersResult: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ListParametersResult",
    "names": Sequence("string"),
    "prefixes": Sequence("string"),
}

LoggerLevel: CoreSchema = {
    "__typename": "rcl_interfaces/msg/LoggerLevel",
    "name": "string",
    "level": "uint32",
}

Log: CoreSchema = {
    "__typename": "rcl_interfaces/msg/Log",
    "stamp": Time,
    "level": "uint8",
    "name": "string",
    "msg": "string",
    "file": "string",
    "function": "string",
    "line": "uint32",
}

ParameterType: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ParameterType",
}

ParameterValue: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ParameterValue",
    "type": "uint8",
    "bool_value": "bool",
    "integer_value": "int64",
    "double_value": "float64",
    "string_value": "string",
    "byte_array_value": Sequence("byte"),
    "bool_array_value": Sequence("bool"),
    "integer_array_value": Sequence("int64"),
    "double_array_value": Sequence("float64"),
    "string_array_value": Sequence("string"),
}

SetLoggerLevelsResult: CoreSchema = {
    "__typename": "rcl_interfaces/msg/SetLoggerLevelsResult",
    "successful": "bool",
    "reason": "string",
}

SetParametersResult: CoreSchema = {
    "__typename": "rcl_interfaces/msg/SetParametersResult",
    "successful": "bool",
    "reason": "string",
}

ParameterDescriptor: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ParameterDescriptor",
    "name": "string",
    "type": "uint8",
    "description": "string",
    "additional_constraints": "string",
    "read_only": "bool",
    "dynamic_typing": "bool",
    "floating_point_range": Sequence(FloatingPointRange, 1),
    "integer_range": Sequence(IntegerRange, 1),
}

Parameter: CoreSchema = {
    "__typename": "rcl_interfaces/msg/Parameter",
    "name": "string",
    "value": ParameterValue,
}

ParameterEventDescriptors: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ParameterEventDescriptors",
    "new_parameters": Sequence(ParameterDescriptor),
    "changed_parameters": Sequence(ParameterDescriptor),
    "deleted_parameters": Sequence(ParameterDescriptor),
}

ParameterEvent: CoreSchema = {
    "__typename": "rcl_interfaces/msg/ParameterEvent",
    "stamp": Time,
    "node": "string",
    "new_parameters": Sequence(Parameter),
    "changed_parameters": Sequence(Parameter),
    "deleted_parameters": Sequence(Parameter),
}

__all__ = [
    "FloatingPointRange",
    "IntegerRange",
    "ListParametersResult",
    "LoggerLevel",
    "Log",
    "ParameterType",
    "ParameterValue",
    "SetLoggerLevelsResult",
    "SetParametersResult",
    "ParameterDescriptor",
    "Parameter",
    "ParameterEventDescriptors",
    "ParameterEvent",
]
