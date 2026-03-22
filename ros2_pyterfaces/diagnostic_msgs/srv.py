from dataclasses import dataclass, field

from ..diagnostic_msgs.msg import DiagnosticStatus
from ..idl import IdlService, IdlStruct, types

__all__ = [
    "AddDiagnostics",
    "AddDiagnostics_Request",
    "AddDiagnostics_Response",
    "SelfTest",
    "SelfTest_Request",
    "SelfTest_Response",
]


@dataclass
class AddDiagnostics_Request(
    IdlStruct, typename="diagnostic_msgs/srv/AddDiagnostics_Request"
):
    load_namespace: str = ""


@dataclass
class AddDiagnostics_Response(
    IdlStruct, typename="diagnostic_msgs/srv/AddDiagnostics_Response"
):
    success: bool = False
    message: str = ""


class AddDiagnostics(IdlService, typename="diagnostic_msgs/srv/AddDiagnostics"):
    Request = AddDiagnostics_Request
    Response = AddDiagnostics_Response


@dataclass
class SelfTest_Request(IdlStruct, typename="diagnostic_msgs/srv/SelfTest_Request"):
    pass


@dataclass
class SelfTest_Response(IdlStruct, typename="diagnostic_msgs/srv/SelfTest_Response"):
    id: str = ""
    passed: types.byte = 0
    status: types.sequence[DiagnosticStatus] = field(default_factory=list)


class SelfTest(IdlService, typename="diagnostic_msgs/srv/SelfTest"):
    Request = SelfTest_Request
    Response = SelfTest_Response
