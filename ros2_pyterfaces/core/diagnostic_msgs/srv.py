from .. import Array, BoundedString, CoreSchema, Sequence, make_srv_schema

from ..diagnostic_msgs.msg import DiagnosticStatus

AddDiagnostics_Request: CoreSchema = {
    "__typename": "diagnostic_msgs/srv/AddDiagnostics_Request",
    "load_namespace": "string",
}

AddDiagnostics_Response: CoreSchema = {
    "__typename": "diagnostic_msgs/srv/AddDiagnostics_Response",
    "success": "bool",
    "message": "string",
}

SelfTest_Request: CoreSchema = {
    "__typename": "diagnostic_msgs/srv/SelfTest_Request",
}

SelfTest_Response: CoreSchema = {
    "__typename": "diagnostic_msgs/srv/SelfTest_Response",
    "id": "string",
    "passed": "byte",
    "status": Sequence(DiagnosticStatus),
}

AddDiagnostics: CoreSchema = make_srv_schema(AddDiagnostics_Request, AddDiagnostics_Response, typename="diagnostic_msgs/srv/AddDiagnostics")
AddDiagnostics_Event: CoreSchema = AddDiagnostics["event_message"]

SelfTest: CoreSchema = make_srv_schema(SelfTest_Request, SelfTest_Response, typename="diagnostic_msgs/srv/SelfTest")
SelfTest_Event: CoreSchema = SelfTest["event_message"]

__all__ = [
    "AddDiagnostics_Request",
    "AddDiagnostics_Response",
    "SelfTest_Request",
    "SelfTest_Response",
    "AddDiagnostics_Event",
    "AddDiagnostics",
    "SelfTest_Event",
    "SelfTest",
]
