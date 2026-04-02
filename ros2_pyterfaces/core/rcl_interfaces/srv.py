from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..rcl_interfaces.msg import ListParametersResult, LoggerLevel, Parameter, ParameterDescriptor, ParameterValue, SetLoggerLevelsResult, SetParametersResult

DescribeParameters_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/DescribeParameters_Request",
    "names": Sequence("string"),
}

DescribeParameters_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/DescribeParameters_Response",
    "descriptors": Sequence(ParameterDescriptor),
}

GetLoggerLevels_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetLoggerLevels_Request",
    "names": Sequence("string"),
}

GetLoggerLevels_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetLoggerLevels_Response",
    "levels": Sequence(LoggerLevel),
}

GetParameters_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetParameters_Request",
    "names": Sequence("string"),
}

GetParameters_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetParameters_Response",
    "values": Sequence(ParameterValue),
}

GetParameterTypes_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetParameterTypes_Request",
    "names": Sequence("string"),
}

GetParameterTypes_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/GetParameterTypes_Response",
    "types": Sequence("uint8"),
}

ListParameters_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/ListParameters_Request",
    "prefixes": Sequence("string"),
    "depth": "uint64",
}

ListParameters_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/ListParameters_Response",
    "result": ListParametersResult,
}

SetLoggerLevels_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetLoggerLevels_Request",
    "levels": Sequence(LoggerLevel),
}

SetLoggerLevels_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetLoggerLevels_Response",
    "results": Sequence(SetLoggerLevelsResult),
}

SetParametersAtomically_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetParametersAtomically_Request",
    "parameters": Sequence(Parameter),
}

SetParametersAtomically_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetParametersAtomically_Response",
    "result": SetParametersResult,
}

SetParameters_Request: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetParameters_Request",
    "parameters": Sequence(Parameter),
}

SetParameters_Response: CoreSchema = {
    "__typename": "rcl_interfaces/srv/SetParameters_Response",
    "results": Sequence(SetParametersResult),
}

DescribeParameters: CoreSchema = make_srv_schema(DescribeParameters_Request, DescribeParameters_Response, typename="rcl_interfaces/srv/DescribeParameters")
DescribeParameters_Event: CoreSchema = DescribeParameters["event_message"]

GetLoggerLevels: CoreSchema = make_srv_schema(GetLoggerLevels_Request, GetLoggerLevels_Response, typename="rcl_interfaces/srv/GetLoggerLevels")
GetLoggerLevels_Event: CoreSchema = GetLoggerLevels["event_message"]

GetParameters: CoreSchema = make_srv_schema(GetParameters_Request, GetParameters_Response, typename="rcl_interfaces/srv/GetParameters")
GetParameters_Event: CoreSchema = GetParameters["event_message"]

GetParameterTypes: CoreSchema = make_srv_schema(GetParameterTypes_Request, GetParameterTypes_Response, typename="rcl_interfaces/srv/GetParameterTypes")
GetParameterTypes_Event: CoreSchema = GetParameterTypes["event_message"]

ListParameters: CoreSchema = make_srv_schema(ListParameters_Request, ListParameters_Response, typename="rcl_interfaces/srv/ListParameters")
ListParameters_Event: CoreSchema = ListParameters["event_message"]

SetLoggerLevels: CoreSchema = make_srv_schema(SetLoggerLevels_Request, SetLoggerLevels_Response, typename="rcl_interfaces/srv/SetLoggerLevels")
SetLoggerLevels_Event: CoreSchema = SetLoggerLevels["event_message"]

SetParametersAtomically: CoreSchema = make_srv_schema(SetParametersAtomically_Request, SetParametersAtomically_Response, typename="rcl_interfaces/srv/SetParametersAtomically")
SetParametersAtomically_Event: CoreSchema = SetParametersAtomically["event_message"]

SetParameters: CoreSchema = make_srv_schema(SetParameters_Request, SetParameters_Response, typename="rcl_interfaces/srv/SetParameters")
SetParameters_Event: CoreSchema = SetParameters["event_message"]

__all__ = [
    "DescribeParameters_Request",
    "DescribeParameters_Response",
    "GetLoggerLevels_Request",
    "GetLoggerLevels_Response",
    "GetParameters_Request",
    "GetParameters_Response",
    "GetParameterTypes_Request",
    "GetParameterTypes_Response",
    "ListParameters_Request",
    "ListParameters_Response",
    "SetLoggerLevels_Request",
    "SetLoggerLevels_Response",
    "SetParametersAtomically_Request",
    "SetParametersAtomically_Response",
    "SetParameters_Request",
    "SetParameters_Response",
    "DescribeParameters_Event",
    "DescribeParameters",
    "GetLoggerLevels_Event",
    "GetLoggerLevels",
    "GetParameters_Event",
    "GetParameters",
    "GetParameterTypes_Event",
    "GetParameterTypes",
    "ListParameters_Event",
    "ListParameters",
    "SetLoggerLevels_Event",
    "SetLoggerLevels",
    "SetParametersAtomically_Event",
    "SetParametersAtomically",
    "SetParameters_Event",
    "SetParameters",
]
