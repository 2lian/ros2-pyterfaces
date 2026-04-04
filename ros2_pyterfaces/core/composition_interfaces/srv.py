from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..rcl_interfaces.msg import Parameter

ListNodes_Request: CoreSchema = {
    "__typename": "composition_interfaces/srv/ListNodes_Request",
}

ListNodes_Response: CoreSchema = {
    "__typename": "composition_interfaces/srv/ListNodes_Response",
    "full_node_names": Sequence("string"),
    "unique_ids": Sequence("uint64"),
}

LoadNode_Request: CoreSchema = {
    "__typename": "composition_interfaces/srv/LoadNode_Request",
    "package_name": "string",
    "plugin_name": "string",
    "node_name": "string",
    "node_namespace": "string",
    "log_level": "uint8",
    "remap_rules": Sequence("string"),
    "parameters": Sequence(Parameter),
    "extra_arguments": Sequence(Parameter),
}

LoadNode_Response: CoreSchema = {
    "__typename": "composition_interfaces/srv/LoadNode_Response",
    "success": "bool",
    "error_message": "string",
    "full_node_name": "string",
    "unique_id": "uint64",
}

UnloadNode_Request: CoreSchema = {
    "__typename": "composition_interfaces/srv/UnloadNode_Request",
    "unique_id": "uint64",
}

UnloadNode_Response: CoreSchema = {
    "__typename": "composition_interfaces/srv/UnloadNode_Response",
    "success": "bool",
    "error_message": "string",
}

ListNodes: CoreSchema = make_srv_schema(ListNodes_Request, ListNodes_Response, typename="composition_interfaces/srv/ListNodes")
ListNodes_Event: CoreSchema = ListNodes["event_message"]

LoadNode: CoreSchema = make_srv_schema(LoadNode_Request, LoadNode_Response, typename="composition_interfaces/srv/LoadNode")
LoadNode_Event: CoreSchema = LoadNode["event_message"]

UnloadNode: CoreSchema = make_srv_schema(UnloadNode_Request, UnloadNode_Response, typename="composition_interfaces/srv/UnloadNode")
UnloadNode_Event: CoreSchema = UnloadNode["event_message"]

__all__ = [
    "ListNodes_Request",
    "ListNodes_Response",
    "LoadNode_Request",
    "LoadNode_Response",
    "UnloadNode_Request",
    "UnloadNode_Response",
    "ListNodes_Event",
    "ListNodes",
    "LoadNode_Event",
    "LoadNode",
    "UnloadNode_Event",
    "UnloadNode",
]
