from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

Empty_Request: CoreSchema = {
    "__typename": "std_srvs/srv/Empty_Request",
}

Empty_Response: CoreSchema = {
    "__typename": "std_srvs/srv/Empty_Response",
}

SetBool_Request: CoreSchema = {
    "__typename": "std_srvs/srv/SetBool_Request",
    "data": "bool",
}

SetBool_Response: CoreSchema = {
    "__typename": "std_srvs/srv/SetBool_Response",
    "success": "bool",
    "message": "string",
}

Trigger_Request: CoreSchema = {
    "__typename": "std_srvs/srv/Trigger_Request",
}

Trigger_Response: CoreSchema = {
    "__typename": "std_srvs/srv/Trigger_Response",
    "success": "bool",
    "message": "string",
}

Empty: CoreSchema = make_srv_schema(Empty_Request, Empty_Response, typename="std_srvs/srv/Empty")
Empty_Event: CoreSchema = Empty["event_message"]

SetBool: CoreSchema = make_srv_schema(SetBool_Request, SetBool_Response, typename="std_srvs/srv/SetBool")
SetBool_Event: CoreSchema = SetBool["event_message"]

Trigger: CoreSchema = make_srv_schema(Trigger_Request, Trigger_Response, typename="std_srvs/srv/Trigger")
Trigger_Event: CoreSchema = Trigger["event_message"]

__all__ = [
    "Empty_Request",
    "Empty_Response",
    "SetBool_Request",
    "SetBool_Response",
    "Trigger_Request",
    "Trigger_Response",
    "Empty_Event",
    "Empty",
    "SetBool_Event",
    "SetBool",
    "Trigger_Event",
    "Trigger",
]
