from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..type_description_interfaces.msg import KeyValue, TypeDescription, TypeSource

GetTypeDescription_Request: CoreSchema = {
    "__typename": "type_description_interfaces/srv/GetTypeDescription_Request",
    "type_name": "string",
    "type_hash": "string",
    "include_type_sources": "bool",
}

GetTypeDescription_Response: CoreSchema = {
    "__typename": "type_description_interfaces/srv/GetTypeDescription_Response",
    "successful": "bool",
    "failure_reason": "string",
    "type_description": TypeDescription,
    "type_sources": Sequence(TypeSource),
    "extra_information": Sequence(KeyValue),
}

GetTypeDescription: CoreSchema = make_srv_schema(GetTypeDescription_Request, GetTypeDescription_Response, typename="type_description_interfaces/srv/GetTypeDescription")
GetTypeDescription_Event: CoreSchema = GetTypeDescription["event_message"]

__all__ = [
    "GetTypeDescription_Request",
    "GetTypeDescription_Response",
    "GetTypeDescription_Event",
    "GetTypeDescription",
]
